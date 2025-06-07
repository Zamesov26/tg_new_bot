from sqlalchemy import select

from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.models import UpdateCallBackQuery
from app.bot_engine.update_context import UpdateContext
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.models import Media
from app.users.models import User


@log_user_action("main_menu")
async def main_menu(ctx: UpdateContext, *args):
    message_image_path = "images/logo.png"
    user = await ctx.store.user.get_by_id(
        ctx.db_session, ctx.update.from_user.tg_id
    )
    if not user:
        user = User(
            tg_id=ctx.update.from_user.tg_id,
            user_name=ctx.update.from_user.username,
            first_name=ctx.update.from_user.first_name,
            last_name=ctx.update.from_user.last_name,
            langue_code=ctx.update.from_user.language_code,
        )
        ctx.db_session.add(user)
        await ctx.db_session.commit()

    text = (
        "Добро пожаловать в Wonderland — волшебный мир шоу пузырей и весёлых аниматоров!\n"
        "Чем могу помочь?"
    )
    keyboard = inline_keyboard_builder(
        [
            [("🎭 Программы и заказ", "choosing_program")],
            [("🎁 Акции", "promo")],
            [("❓ Частые вопросы", "viewing_faq")],
            [("📞 Связаться с нами", "feedback_input")],
        ]
    )
    image_file = (
        await ctx.db_session.execute(
            select(Media).where(Media.file_path == message_image_path)
        )
    ).scalar_one_or_none()
    if isinstance(ctx.update, UpdateCallBackQuery):
        answer = await ctx.store.tg_api.edit_message_media(
            chat_id=ctx.update.get_chat_id(),
            message_id=ctx.update.get_message_id(),
            file_id=image_file.file_id if image_file else None,
            file_path=message_image_path,
            caption=text,
            reply_markup=keyboard,
        )
    else:
        answer = await ctx.store.tg_api.send_photo(
            chat_id=ctx.update.get_chat_id(),
            caption=text,
            path_image=message_image_path,
            file_id=image_file.file_id if image_file else None,
            reply_markup=keyboard,
        )
    if not image_file:
        promo_image = Media(
            title="promo_image",
            file_id=answer["result"]["photo"][0]["file_id"],
            file_path=message_image_path,
        )
        ctx.db_session.add(promo_image)
        await ctx.db_session.commit()
    return answer
