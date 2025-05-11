from app.bot.models import UpdateCallBackQuery
from app.store import Store


async def delete_message(update: UpdateCallBackQuery, store: Store, *args):
    await store.tg_api.delete_message(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
    )
