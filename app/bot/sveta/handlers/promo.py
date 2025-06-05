from datetime import date

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.models import UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.promo.models import Promo
from app.store import Store

PROMO_TEMPLATE = """🎉 {title}$
💸 {new_price}$
📝{short_description}
📅 До:  {end_date}
"""


async def promo(
    update: "UpdateMessage", store: "Store", db_session: AsyncSession, *args
):
    keyboard = inline_keyboard_builder(
        [
            # [("⬅️ Назад", "TODO"), ("➡️ Далее", "TODO")],
            [("🔙 Меню", "main_menu")],
        ]
    )
    today = date.today()
    stms = select(Promo).where(
        Promo.is_active,
        or_(Promo.start_date == None, Promo.start_date <= today),
        or_(Promo.end_date == None, Promo.end_date >= today),
    )
    res = await db_session.execute(stms)
    promos = list(res.scalars().all())
    if not promos:
        return await store.tg_api.edit_message_media(
            chat_id=update.get_chat_id(),
            message_id=update.get_message_id(),
            caption="Нету действующийх акций",
            # file_id="AgACAgIAAxkDAAIewmgkTFVQwFE2vyUqMmVUbHQOO6UTAALI7DEbtLQoSWaxos7VuSZ6AQADAgADcwADNgQ",
            file_path="images/promo.png",
            reply_markup=keyboard,
        )
    texts = []
    for promo_item in promos:
        texts.append(PROMO_TEMPLATE.format(
            title=promo_item.title,
            old_price=promo_item.old_price,
            new_price=promo_item.new_price,
            short_description=promo_item.short_description,
            end_date=promo_item.end_date
        ))
    
    return await store.tg_api.edit_message_media(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
        caption='---------------------------\n'.join(texts),
        # file_id="AgACAgIAAxkDAAIewmgkTFVQwFE2vyUqMmVUbHQOO6UTAALI7DEbtLQoSWaxos7VuSZ6AQADAgADcwADNgQ",
        file_path="images/promo.png",
        reply_markup=keyboard,
    )
