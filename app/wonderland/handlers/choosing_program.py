from sqlalchemy import select

from app.actions.user_actions.decorators import log_user_action
from app.bot_engine.update_context import Context
from app.bot_engine.utils import inline_keyboard_builder
from app.medias.decorators import with_image_file
from app.medias.models import Media

PROGRAM_MESSAGE_IMAGE_PATH = "images/programs.png"
TEMPLATE = """{title} - {price}$
{short_description}
"""
COUNT_COLUMNS = 2


def chunk_list(lst, chunk_size):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


@log_user_action("programs")
@with_image_file(PROGRAM_MESSAGE_IMAGE_PATH)
async def programs(ctx: Context, image_file: Media | None, *args, **kwargs):
    program_list = await ctx.store.program.get_all(ctx.db_session)
    texts = []
    buttons = []

    for item in program_list:
        texts.append(
            TEMPLATE.format(
                title=item.title,
                price=item.price,
                short_description=item.short_description,
            )
        )
        buttons.append([item.title, "program_details:{id}".format(id=item.id)])

    buttons = chunk_list(buttons, 2)
    buttons.append(
        [["🔙 Назад", "main_menu"]],
    )
    keyboard = inline_keyboard_builder(buttons)

    answer = await ctx.store.tg_api.edit_message_media(
        chat_id=ctx.event.get_chat_id(),
        message_id=ctx.event.get_message_id(),
        file_id=image_file.file_id if image_file else None,
        file_path="images/programs.png",
        caption="\n".join(texts),
        reply_markup=keyboard,
    )
    return answer


@log_user_action("program_details")
async def program_details(ctx: Context, *args, **kwargs):
    _, program = ctx.event.callback_query.data.split(":")
    program_item = await ctx.store.program.get_by_id(
        ctx.db_session, int(program)
    )
    text = program_item.description or program_item.short_description
    keyboard = inline_keyboard_builder(
        [
            [["✅ Заказать", f"entering_date"]],
            [["❌ Убрать", f"remove_message"]],
        ]
    )
    # TODO: удалять прошлое сообщение либо хотябы убирать из него клавиатуру.
    # TODO: брать из базы
    await ctx.store.tg_api.send_media_group(
        chat_id=ctx.event.get_chat_id(),
        media_items=[
            {
                "type": "photo",
                "file_id": "AgACAgIAAxkDAAIewmgkTFVQwFE2vyUqMmVUbHQOO6UTAALI7DEbtLQoSWaxos7VuSZ6AQADAgADcwADNgQ",
                "caption": text,
            },
            {
                "type": "photo",
                "file_id": "AgACAgIAAxkDAAIewWgkRhfhhz1IQa6nzL5GIKyNM0QrAAJd9DEbGhkgSRE3-vJU6jNjAQADAgADeAADNgQ",
            },
            {
                "type": "photo",
                "file_id": "AgACAgIAAxkDAAIev2gkRUYxl76b6bLhz1jAuqdSLzs-AAJt7DEbtLQoSUHuX48UhUsSAQADAgADeAADNgQ",
            },
        ],
        reply_markup=keyboard,
    )
    keyboard = inline_keyboard_builder(
        [
            [["📅 Забронировать", f"order_start"]],
            [["🔙 Программы", f"choosing_program"]],
        ]
    )
    await ctx.store.tg_api.send_message(
        chat_id=ctx.event.get_chat_id(),
        text="Возврат к выбору",
        reply_markup=keyboard,
    )


@log_user_action("entering_date")
async def entering_date(ctx: Context, *args, **kwargs):
    # TODO
    text = "Тут будет описанно торговое предложение и переход к оформлению/заполнение анкеты"
    keyboard = inline_keyboard_builder(
        [
            [["📝 Оформить", f"TODO"]],
            [["❌ Убрать", f"remove_message"]],
        ]
    )

    await ctx.store.tg_api.send_message(
        chat_id=ctx.event.get_chat_id(),
        text=text,
        reply_markup=keyboard,
    )
