import asyncio
import datetime
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.game_bot.constants import (
    CURRENT_QUESTION,
    CURRENT_THEME,
    GameImages,
    States,
    Timers,
)
from app.bot.game_bot.handlers.general import send_category_list
from app.bot.utils import inline_keyboard_builder, inline_keyboard_game_builder
from app.own_game.models.games import Game

if typing.TYPE_CHECKING:
    from app.bot.models import UpdateCallBackQuery
    from app.store.store import Store


async def choice_theme(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):
    _, user_tg_id, category_id = update.callback_query.data.split(":")
    if int(user_tg_id) != update.callback_query.from_user.id:
        await store.tg_api.answer_callback_query(update.callback_query.id)
        return

    game.state = States.CHOICE_QUESTION
    store.redis.set_state(game.chat_id, States.CHOICE_QUESTION)
    await store.rabbit.delete_message(
        chat_id=game.chat_id,
        message_id=update.callback_query.message.message_id,
    )
    game_questions = await store.game.get_available_questions(
        db_session, game.id, int(category_id)
    )
    category = await store.question.get_category_by_id(
        db_session, int(category_id)
    )
    await db_session.commit()

    keyboard = [
        [
            (question.price, f"price:{user_tg_id}:{question.question_id}")
            for question in game_questions
        ]
    ]
    keyboard.append([("Назад", "back")])

    message = await store.tg_api.send_photo(
        chat_id=update.callback_query.message.chat.id,
        photo_url=GameImages.CHOICE_QUESTION,
        caption=CURRENT_THEME % category.name,
        reply_markup=inline_keyboard_builder(
            keyboard,
        ),
    )
    store.redis.set_last_message(game.chat_id, message_id=message.message_id)


async def back_to_theme(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):
    active_user = await store.user.get_by_id(db_session, game.active_user_id)
    if active_user.tg_id != update.callback_query.from_user.id:
        await store.tg_api.answer_callback_query(update.callback_query.id)
        return
    await store.rabbit.delete_message(
        chat_id=game.chat_id,
        message_id=update.callback_query.message.message_id,
    )
    send_message_coroutine = await send_category_list(
        store=store,
        db_session=db_session,
        game=game,
        player_name=active_user.name,
        player_tg_id=active_user.tg_id,
    )
    await db_session.commit()

    message = await send_message_coroutine
    store.redis.set_last_message(game.chat_id, message_id=message.message_id)


async def choice_price(
    update: "UpdateCallBackQuery", store: "Store", db_session, game: "Game"
):
    _, user_tg_id, question_id = update.callback_query.data.split(":")
    question_id = int(question_id)
    if int(user_tg_id) != update.callback_query.from_user.id:
        await store.tg_api.answer_callback_query(update.callback_query.id)
        return

    game.state = States.WAITING_PLAYER
    store.redis.set_state(game.chat_id, States.WAITING_PLAYER)
    await store.rabbit.delete_message(
        chat_id=game.chat_id,
        message_id=update.callback_query.message.message_id,
    )
    question = await store.question.get_queestion_by_id(db_session, question_id)
    game.active_question_id = question.id

    keyboard = inline_keyboard_game_builder(
        [[("Отвечать", f"click:all_users:{question.id}")]]
    )
    end_time = int(datetime.datetime.now(datetime.UTC).timestamp())
    await store.game.update_game_question(
        db_session=db_session,
        game_id=game.id,
        question_id=question.id,
        end_time=end_time,
    )
    await db_session.commit()

    message = await store.tg_api.send_photo(
        chat_id=update.callback_query.message.chat.id,
        photo_url=GameImages.QUESTION,
        caption=CURRENT_QUESTION % question.title,
        reply_markup=keyboard,
    )
    store.redis.set_last_message(
        chat_id=game.chat_id, message_id=message.message_id
    )
    asyncio.create_task(
        time_limit_answer(
            chat_id=game.chat_id,
            game_id=game.id,
            message_id=update.callback_query.message.message_id,
            question_id=question.id,
            store=store,
            true_answer=question.answer,
        )
    )


async def time_limit_answer(
    chat_id: int,
    game_id: int,
    message_id: int,
    question_id: int,
    store: "Store",
    true_answer,
    time_limit=Timers.WAITING_PLAYER,
) -> int | None:
    db_session = store.game.app.database.session()
    while True:
        await asyncio.sleep(time_limit)
        async with store.game.app.database.session() as db_session:
            game_question = await store.game.get_game_question(
                db_session, game_id, question_id
            )
        if not game_question:
            return
        current_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
        if current_time < game_question.end_time:
            time_limit = game_question.end_time - current_time
            continue
        break
    store.redis.set_state(chat_id, States.WAITING_ANSWER)
    await store.rabbit.edit_message_reply_markup(chat_id, message_id)
    text = "Время вышло\nПравильный ответ: %s"
    await store.tg_api.send_message(chat_id=chat_id, text=text % true_answer)

    db_session = store.game.app.database.session()
    async with db_session.begin():
        game = await store.game.get_game_by_id(db_session, game_id)
        if game.active_question_id != question_id:
            await store.tg_api.answer_callback_query(update.callback_query.id)
            return
        if game.state == States.WAITING_ANSWER:
            game.state = States.CHOICE_THEME
            game_question = await store.game.get_game_question(
                db_session, game_id, question_id
            )
            await store.game.change_user_point_by_user_id(
                db_session,
                game_id,
                game.responding_user_id,
                -game_question.price,
            )
        else:
            game.state = States.CHOICE_THEME
            message_id = store.redis.get_last_message(
                chat_id=game.chat_id, with_deletion=True
            )
            if message_id:
                await store.rabbit.edit_message_reply_markup(
                    chat_id=game.chat_id, message_id=message_id
                )

        await store.game.update_game_question(
            db_session, game.id, question_id, is_available=False
        )
        send_message_coroutine = await send_category_list(
            store=store,
            db_session=db_session,
            game=game,
            player_name=game.active_user.name,
            player_tg_id=game.active_user.tg_id,
        )
        await db_session.commit()
        message = await send_message_coroutine
        store.redis.set_last_message(
            chat_id=game.chat_id, message_id=message.message_id
        )
