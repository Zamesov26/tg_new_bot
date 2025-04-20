import datetime
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.game_bot.constants import (
    CURRENT_QUESTION,
    FALSE_ANSWER,
    TRUE_ANSWER,
    GameImages,
    States,
    Timers,
)
from app.bot.game_bot.handlers.general import send_category_list
from app.bot.game_bot.utils import players_to_text_grid
from app.bot.utils import inline_keyboard_game_builder

if typing.TYPE_CHECKING:
    from app.bot.models import UpdateMessage
    from app.own_game.models.games import Game
    from app.store.store import Store


async def some_answer(
    update: "UpdateMessage",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):
    user_answer = update.message.text
    responding_user = await store.user.get_by_id(
        db_session, game.responding_user_id
    )
    if responding_user.tg_id != update.message.from_user.id:
        return
    question = game.active_question
    if user_answer.lower() != question.answer.lower():
        game.state = States.WAITING_PLAYER
        store.redis.set_state(game.chat_id, States.WAITING_PLAYER)
        end_time = (
            int(datetime.datetime.now(datetime.UTC).timestamp())
            + Timers.WAITING_PLAYER_BEFORE_BAD_ANSWER
        )
        await store.game.update_game_question(
            db_session, game.id, question.id, end_time=end_time
        )
        await store.game.change_user_point(
            db_session,
            game.id,
            update.message.from_user.id,
            question.id,
            is_increase=False,
        )
        players = await store.game.get_active_players_in_game(
            db_session, game.id
        )
        text_players = players_to_text_grid(players)

        await db_session.commit()
        await store.tg_api.send_photo(
            chat_id=update.message.chat.id,
            photo_url=GameImages.FALSE_ANSWER,
            caption=FALSE_ANSWER % text_players,
        )
        keyboard = inline_keyboard_game_builder(
            [[("Отвечать", f"click:{question.id}")]]
        )
        message = await store.tg_api.send_photo(
            chat_id=update.message.chat.id,
            photo_url=GameImages.QUESTION,
            caption=CURRENT_QUESTION % question.title,
            reply_markup=keyboard,
        )
        store.redis.set_last_message(
            chat_id=game.chat_id, message_id=message.message_id
        )
        return
    await store.game.update_game_question(
        db_session, game.id, question.id, is_available=False
    )
    await store.game.change_user_point(
        db_session,
        game.id,
        update.message.from_user.id,
        question.id,
        is_increase=True,
    )
    players = await store.game.get_active_players_in_game(db_session, game.id)
    players_text = players_to_text_grid(players)

    send_message_coroutine = await send_category_list(
        store=store,
        db_session=db_session,
        game=game,
        player_name=responding_user.name,
        player_tg_id=responding_user.tg_id,
    )
    await db_session.commit()
    await store.tg_api.send_photo(
        chat_id=update.message.chat.id,
        photo_url=GameImages.TRUE_ANSWER,
        caption=TRUE_ANSWER % players_text,
    )
    message = await send_message_coroutine
    store.redis.set_last_message(
        chat_id=game.chat_id, message_id=message.message_id
    )
