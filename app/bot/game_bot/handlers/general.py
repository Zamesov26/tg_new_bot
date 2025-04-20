import json
import typing

import pika
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.game_bot.constants import CURRENT_TURN, GameImages, States
from app.bot.game_bot.utils import get_category_keyboard, players_to_text_grid

if typing.TYPE_CHECKING:
    from app.bot.models import (
        UpdateCallBackQuery,
        UpdateMessage,
        UpdateMyChatMember,
    )
    from app.own_game.models.games import Game
    from app.store.store import Store


async def no_active_game(update: "UpdateCallBackQuery", store: "Store", *args):
    await store.tg_api.edit_message_text(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        text="Игра больше не активна",
    )


async def stop(
    update: "UpdateMessage",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):

    if not game:
        await store.tg_api.send_message(
            chat_id=update.message.chat.id,
            text="Нету активных игр",
        )
        return
    await store.game.update_game_question(
        db_session, game.id, game.active_question_id, is_available=False
    )

    store.redis.delete_state(game.chat_id)
    store.redis.delete_active_players(game.chat_id)
    game.state = States.GAME_STOPPED
    game.is_active = False
    await db_session.commit()

    last_message = store.redis.get_last_message(
        update.message.chat.id, with_deletion=True
    )
    if last_message:
        await store.rabbit.edit_message_reply_markup(
            chat_id=game.chat_id, message_id=last_message
        )

    await store.tg_api.send_message(
        chat_id=game.chat_id,
        text="Активная игра остановленна",
    )


async def send_category_list(
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
    player_name: str,
    player_tg_id: int,
) -> typing.Coroutine:
    themes = list(
        await store.game.get_available_categories_by_game(db_session, game.id)
    )
    if not themes:
        game.state = States.GAME_OVER
        game.is_active = False
        players = await store.game.get_active_players_in_game(
            db_session, game.id
        )
        players_text = players_to_text_grid(players)
        text = "Вопросов нет, игра окончена.\nИтоги игры:\n%s"
        return store.tg_api.send_message(
            chat_id=game.chat_id,
            text=text % players_text,
        )
    game.state = States.CHOICE_THEME
    return store.tg_api.send_photo(
        chat_id=game.chat_id,
        photo_url=GameImages.CHOICE_THEME,
        caption=CURRENT_TURN % player_name,
        reply_markup=get_category_keyboard(themes, player_tg_id),
    )


async def say_hello(update: "UpdateMyChatMember", store: "Store", *args):
    text = (
        "Cпасибо, что добавили\n"
        "Бот реагирует на следующие команды\n"
        "/start - для начала игры\n"
        "/stop - для остановки текущей игры"
    )
    await store.tg_api.send_photo(
        chat_id=update.my_chat_member.chat.id,
        photo_url=GameImages.START,
        caption=text,
    )


async def game_help(update: "UpdateMessage", store: "Store", *args):
    text = "тут должен быть список команд, но его нет("
    await store.tg_api.send_photo(
        chat_id=update.message.chat.id,
        photo_url="",
        caption=text,
    )


async def send_message(update: "UpdateMessage", store: "Store", *args):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue="send_message_queue", durable=True)
    body = {"chat_id": update.message.chat.id, "text": "hello"}
    channel.basic_publish(
        exchange="",
        routing_key="send_message_queue",
        body=json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ),
    )
    connection.close()
