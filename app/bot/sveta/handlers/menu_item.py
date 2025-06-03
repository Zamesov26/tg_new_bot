from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from app.bot.models import UpdateCallBackQuery
    from app.store import Store


async def callback_menu_item(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    *args,
):
    _, menu_item_id = update.callback_query.data.split(":")
    texts = []
    buttons = []