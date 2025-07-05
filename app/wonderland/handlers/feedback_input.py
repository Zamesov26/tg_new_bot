from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.update_context import Context
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.decorators import with_image_file
from app.medias.models import Media
from app.tg_api.accessor import TelegramAPIError

MESSAGE_IMAGE_PATH = "images/feedback.png"
TEXT = """Телефон: +1 818 384 0753
tg: @svetlana_zamesova"""


@log_user_action("feedback_input")
@with_image_file(MESSAGE_IMAGE_PATH)
async def feedback_input(
    ctx: Context, image_file: Media | None, *args, **kwargs
):
    keyboard = inline_keyboard_builder(
        [
            # [["профиль", "", "tg://user?id=810659048"]],
            [["профиль", "", "tg://user?id=1051661221"]],
            [["🔙 Меню", f"main_menu"]],
        ]
    )
    try:
        return await ctx.store.tg_api.edit_message_media(
            chat_id=ctx.event.get_chat_id(),
            message_id=ctx.event.get_message_id(),
            file_id=image_file.file_id if image_file else None,
            file_path=MESSAGE_IMAGE_PATH,
            caption=TEXT,
            reply_markup=keyboard,
        )
    except TelegramAPIError:
        keyboard = inline_keyboard_builder(
            [
                [["🔙 Меню", f"main_menu"]],
            ]
        )
        return await ctx.store.tg_api.edit_message_media(
            chat_id=ctx.event.get_chat_id(),
            message_id=ctx.event.get_message_id(),
            file_id=image_file.file_id if image_file else None,
            file_path=MESSAGE_IMAGE_PATH,
            caption=TEXT + "\nПрофиль: скрыт",
            reply_markup=keyboard,
        )
