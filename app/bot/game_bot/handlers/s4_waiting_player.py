import datetime
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.game_bot.constants import States, Timers

if typing.TYPE_CHECKING:
    from app.bot.models import UpdateCallBackQuery
    from app.own_game.models.games import Game
    from app.store.store import Store


async def click_button(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):
    *_, question_id = update.callback_query.data.split(":")
    question_id = int(question_id)
    if not store.redis.is_active_players(
        game.chat_id, update.callback_query.from_user.id
    ):
        await store.tg_api.answer_callback_query(update.callback_query.id)
        return

    store.redis.set_responding_user(
        game.chat_id, update.callback_query.from_user.id
    )
    game.state = States.WAITING_ANSWER
    store.redis.set_state(game.chat_id, States.WAITING_ANSWER)
    user = await store.game.get_user_in_game(
        db_session, game.id, update.callback_query.from_user.id
    )
    game.responding_user_id = user.id

    end_time = (
        int(datetime.datetime.now(datetime.UTC).timestamp())
        + Timers.WAITING_ANSWER
    )
    await store.game.update_game_question(
        db_session, game_id=game.id, question_id=question_id, end_time=end_time
    )
    await db_session.commit()

    text = "Игрок %s\nНапишите ваш вариант ответа!"
    await store.tg_api.edit_message_caption(
        message_id=update.callback_query.message.message_id,
        chat_id=update.callback_query.message.chat.id,
        caption=text % user.name,
    )
