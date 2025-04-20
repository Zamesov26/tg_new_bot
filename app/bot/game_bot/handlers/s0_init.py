import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.game_bot.constants import WAITING_PLAYERS, GameImages, States
from app.bot.utils import inline_keyboard_builder

if typing.TYPE_CHECKING:
    from app.bot.models import UpdateMessage
    from app.store.store import Store


async def new_game(
    update: "UpdateMessage", store: "Store", db_sesstion: AsyncSession, *args
):
    store.redis.set_state(update.message.chat.id, States.PREPARING)
    game = await store.game.create_game(
        db_sesstion, update.message.chat.id, state=States.PREPARING
    )
    await db_sesstion.commit()

    keyboard = inline_keyboard_builder(
        [[("Учавствовать", f"add:{game.id}"), ("Начать", f"go:{game.id}")]]
    )
    message = await store.tg_api.send_photo(
        chat_id=update.message.chat.id,
        caption=WAITING_PLAYERS % "",
        photo_url=GameImages.PREPARING,
        reply_markup=keyboard,
    )

    store.redis.set_last_message(
        chat_id=game.chat_id, message_id=message.message_id
    )
