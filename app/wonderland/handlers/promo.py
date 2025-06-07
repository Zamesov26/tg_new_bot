from datetime import date

from sqlalchemy import select, or_

from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.update_context import UpdateContext
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.models import Media
from app.promo.models import Promo

PROMO_TEMPLATE = """🎉 {title}$
💸 {new_price}$
📝{short_description}
📅 До:  {end_date}
"""


@log_user_action("promo")
async def promo(ctx: UpdateContext, *args):
    message_image_path = "images/promo.png"

    keyboard = inline_keyboard_builder(
        [
            [("🔙 Меню", "main_menu")],
        ]
    )
    today = date.today()
    stmt = select(Promo).where(
        Promo.is_active,
        or_(Promo.start_date == None, Promo.start_date <= today),
        or_(Promo.end_date == None, Promo.end_date >= today),
    )
    res = await ctx.db_session.execute(stmt)
    promos = list(res.scalars().all())
    image_file = (
        await ctx.db_session.execute(
            select(Media).where(Media.file_path == message_image_path)
        )
    ).scalar_one_or_none()
    if not promos:
        answer = await ctx.store.tg_api.edit_message_media(
            chat_id=ctx.update.get_chat_id(),
            message_id=ctx.update.get_message_id(),
            caption="Нет действующийх акций",
            file_id=image_file.file_id if image_file else None,
            file_path=message_image_path,
            reply_markup=keyboard,
        )
        if not image_file:
            promo_image = Media(
                title="promo_image",
                file_id=answer["result"]["photo"][0]["file_id"],
                file_path=message_image_path,
            )
            ctx.db_session.add(promo_image)
        return answer
    texts = []
    for promo_item in promos:
        texts.append(
            PROMO_TEMPLATE.format(
                title=promo_item.title,
                old_price=promo_item.old_price,
                new_price=promo_item.new_price,
                short_description=promo_item.short_description,
                end_date=promo_item.end_date,
            )
        )

    answer = await ctx.store.tg_api.edit_message_media(
        chat_id=ctx.update.get_chat_id(),
        message_id=ctx.update.get_message_id(),
        caption="---------------------------\n".join(texts),
        file_id=image_file.file_id if image_file else None,
        file_path=message_image_path,
        reply_markup=keyboard,
    )
    if not image_file:
        promo_image = Media(
            title="promo_image",
            file_id=answer["result"]["photo"][0]["file_id"],
            file_path=message_image_path,
        )
        ctx.db_session.add(promo_image)
    return answer
