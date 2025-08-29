from datetime import date

from sqlalchemy import or_, select

from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.update_context import Context
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.decorators import fallback_image_file
from app.medias.models import Media
from app.promo.models import Promo

PROMO_IMAGE_PATH = "images/promo.png"
PROMO_TEMPLATE = """🎉 {title}$
💸 {new_price}$
📝{short_description}
📅 До:  {end_date}
"""


@log_user_action("promo")
@fallback_image_file(file_path=PROMO_IMAGE_PATH)
async def promo(ctx: Context, image_file: Media | None, *args, **kwargs):
    keyboard = inline_keyboard_builder(
        [
            [["🔙 Меню", "main_menu"]],
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
    if not promos:
        answer = await ctx.store.tg_api.edit_message_media(
            chat_id=ctx.event.get_chat_id(),
            message_id=ctx.event.get_message_id(),
            caption="Нет действующийх акций",
            file_id=image_file.file_id if image_file else None,
            file_path=PROMO_IMAGE_PATH,
            reply_markup=keyboard,
        )
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
        chat_id=ctx.event.get_chat_id(),
        message_id=ctx.event.get_message_id(),
        caption="---------------------------\n".join(texts),
        file_id=image_file.file_id if image_file else None,
        file_path=PROMO_IMAGE_PATH,
        reply_markup=keyboard,
    )
    return answer
