import json
import typing
from random import choice

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.game_bot.constants import WAITING_PLAYERS, GameSetting, States
from app.bot.game_bot.handlers.general import send_category_list

if typing.TYPE_CHECKING:
    from app.bot.models import UpdateCallBackQuery
    from app.own_game.models.games import Game
    from app.store.store import Store


async def added_user(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):
    user = await store.user.get_by_tg_id(
        db_session, update.callback_query.from_user.id
    )
    if not user:
        user = await store.user.create_user(
            db_session,
            update.callback_query.from_user.id,
            update.callback_query.from_user.first_name,
        )

    await store.game.toggle_palayer_in_game(db_session, game.id, user.id)
    players = await store.game.get_active_players_in_game(db_session, game.id)
    store.redis.add_active_players(game.chat_id, [item[2] for item in players])
    await db_session.commit()
    await store.tg_api.edit_message_caption(
        message_id=update.callback_query.message.message_id,
        chat_id=update.callback_query.message.chat.id,
        caption=WAITING_PLAYERS % "\n".join([p[1] for p in players]),
        reply_markup=update.callback_query.message.reply_markup,
    )


async def go(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    game: "Game",
):
    active_players = store.redis.get_active_players(game.chat_id)
    if not store.redis.is_active_players(
        game.chat_id, update.callback_query.from_user.id
    ):
        await store.tg_api.answer_callback_query(update.callback_query.id)
        await store.tg_api.send_message(
            chat_id=game.chat_id,
            text="Начать может только участник игры",
        )
        return
    if len(active_players) < GameSetting.MIN_NUMBER_PLAYERS:
        await store.tg_api.answer_callback_query(update.callback_query.id)
        await store.tg_api.send_message(
            chat_id=game.chat_id,
            text=(
                "для начала необходимо не менее"
                f"{GameSetting.MIN_NUMBER_PLAYERS} участников"
            ),
        )
        await store.tg_api.answer_callback_query(update.callback_query.id)
        return

    store.redis.set_state(game.chat_id, States.CHOICE_THEME)
    players = await store.game.get_active_players_in_game(db_session, game.id)
    await store.game.assing_random_themes(
        db_session,
        game.id,
        theme_cnt=GameSetting.NUMBER_THEMES,
        question_cnt=GameSetting.NUMBER_QUESTIONS,
    )
    active_player_id, active_player_name, active_player_tg_id, *_ = choice(
        players
    )
    game.active_user_id = active_player_id

    send_message_coroutine = await send_category_list(
        store=store,
        db_session=db_session,
        game=game,
        player_name=active_player_name,
        player_tg_id=active_player_tg_id,
    )
    await db_session.commit()
    await store.rabbit.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
    )
    message = await send_message_coroutine
    store.redis.set_last_message(
        chat_id=game.chat_id, message_id=message.message_id
    )
