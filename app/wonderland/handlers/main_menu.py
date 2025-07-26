from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.update_context import Context
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.decorators import fallback_image_file
from app.medias.models import Media

MAIN_MENU_IMAGE_PATH = "images/logo.png"
TEXT = (
    "Добро пожаловать в Wonderland — волшебный мир шоу пузырей и весёлых аниматоров!\n"
    "Чем могу помочь?"
)
USER_KEYBOARD = inline_keyboard_builder(
    [
        [["🎭 Программы и заказ", "choosing_program"]],
        [["🎁 Акции", "promo"]],
        [["❓ Частые вопросы", "viewing_faq"]],
        [["📞 Связаться с нами", "contacts"]],
    ]
)


@log_user_action("main_menu")
@fallback_image_file(file_path=MAIN_MENU_IMAGE_PATH)
async def main_menu_callback(
    ctx: Context, image_file: Media | None, *args, **kwargs
):
    # TODO:1 пернести в мидлвар или декоратор
    _, created = await ctx.store.user.get_or_create(
        ctx.db_session, ctx.event.from_user
    )
    if created:
        # TODO отправка в брокер
        # TODO есть пользователь у которого скрыт профиль надо это обрабатывать user?id = 1051661221
        link_keyboard = inline_keyboard_builder(
            [
                [["профиль", "", f"tg://user?id={ctx.event.from_user.tg_id}"]],
            ]
        )
        for admin in await ctx.store.admin.get_all(ctx.db_session):
            await ctx.store.tg_api.send_message(
                chat_id=admin.tg_id,
                text="новый пользователь: TODO какие-то данные",
                reply_markup=link_keyboard,
            )
    # TODO:1 End

    answer = await ctx.store.tg_api.edit_message_media(
        chat_id=ctx.event.get_chat_id(),
        message_id=ctx.event.get_message_id(),
        file_id=image_file.file_id if image_file else None,
        file_path=MAIN_MENU_IMAGE_PATH,
        caption=TEXT,
        reply_markup=USER_KEYBOARD,
    )
    return answer


@log_user_action("main_menu")
@fallback_image_file(file_path=MAIN_MENU_IMAGE_PATH)
async def main_menu_command(
    ctx: Context, image_file: Media | None, *args, **kwargs
):
    # TODO:1 пернести в мидлва
    _, created = await ctx.store.user.get_or_create(
        ctx.db_session, ctx.event.from_user
    )
    if created:
        # TODO отправка оповещений через брокер
        # TODO есть пользователь у которого скрыт профиль надо это обрабатывать user?id = 1051661221
        link_keyboard = inline_keyboard_builder(
            [
                [["профиль", "", f"tg://user?id={ctx.event.from_user.tg_id}"]],
            ]
        )
        for admin in await ctx.store.admin.get_all(ctx.db_session):
            await ctx.store.tg_api.send_message(
                chat_id=admin.tg_id,
                text="новый пользователь: TODO какие-то данные",
                reply_markup=link_keyboard,
            )
    # TODO:1 End

    answer = await ctx.store.tg_api.send_photo(
        chat_id=ctx.event.get_chat_id(),
        caption=TEXT,
        path_image=MAIN_MENU_IMAGE_PATH,
        file_id=image_file.file_id if image_file else None,
        reply_markup=USER_KEYBOARD,
    )
    return answer
