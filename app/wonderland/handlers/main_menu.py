from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.models import UpdateCallBackQuery
from app.bot_engine.update_context import UpdateContext
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.decorators import with_image_file
from app.medias.models import Media

MESSAGE_IMAGE_PATH = "images/logo.png"
TEXT = (
    "Добро пожаловать в Wonderland — волшебный мир шоу пузырей и весёлых аниматоров!\n"
    "Чем могу помочь?"
)
USER_KEYBOARD = inline_keyboard_builder(
    [
        [("🎭 Программы и заказ", "choosing_program")],
        [("🎁 Акции", "promo")],
        [("❓ Частые вопросы", "viewing_faq")],
        [("📞 Связаться с нами", "feedback_input")],
    ]
)


@log_user_action("main_menu")
@with_image_file(MESSAGE_IMAGE_PATH)
async def main_menu(
    ctx: UpdateContext, image_file: Media | None, *args, **kwargs
):
    _, created = await ctx.store.user.get_or_create(
        ctx.db_session, ctx.update.from_user
    )
    if created:
        print("создан новый пользователь оправляем уведомление администраторам")

    if isinstance(ctx.update, UpdateCallBackQuery):
        answer = await ctx.store.tg_api.edit_message_media(
            chat_id=ctx.update.get_chat_id(),
            message_id=ctx.update.get_message_id(),
            file_id=image_file.file_id if image_file else None,
            file_path=MESSAGE_IMAGE_PATH,
            caption=TEXT,
            reply_markup=USER_KEYBOARD,
        )
    else:
        answer = await ctx.store.tg_api.send_photo(
            chat_id=ctx.update.get_chat_id(),
            caption=TEXT,
            path_image=MESSAGE_IMAGE_PATH,
            file_id=image_file.file_id if image_file else None,
            reply_markup=USER_KEYBOARD,
        )
    return answer
