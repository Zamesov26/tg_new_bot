from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.models import UpdateCallBackQuery
from app.bot.utils import inline_keyboard_builder
from app.store import Store

TEMPLATE = """{title} - {price}$
{short_description}
"""
COUNT_COLUMNS = 2


def chunk_list(lst, chunk_size):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


async def programs(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    *args,
):
    program_list = await store.program.get_all(db_session)
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
        buttons.append((item.title, "program_details:{id}".format(id=item.id)))

    buttons = chunk_list(buttons, 2)
    buttons.append(
        [("🔙 Назад", "main_menu")],
    )
    keyboard = inline_keyboard_builder(buttons)

    # TODO: надо подумать как это сделать универсально, чтобы можно было использовать во всех други ручках
    # TODO: получить картинку из базы
    #   как понимаем какую картинку нужно вернуть?
    #   наверно может быть ситуация когда картинка не нужна вообще
    # TODO: подставить данные в функцию
    res_photo = await store.tg_api.edit_message_media(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
        file_id="AgACAgIAAxkDAAIewWgkRhfhhz1IQa6nzL5GIKyNM0QrAAJd9DEbGhkgSRE3-vJU6jNjAQADAgADeAADNgQ",
        file_path="images/programs.png",
        caption="\n".join(texts),
        reply_markup=keyboard,
    )
    # TODO: если нету file_id то добавить в базу


async def program_details(
    update: "UpdateCallBackQuery",
    store: "Store",
    db_session: AsyncSession,
    *args,
):
    _, program = update.callback_query.data.split(":")
    program_item = await store.program.get_by_id(db_session, int(program))
    text = program_item.description or program_item.short_description
    keyboard = inline_keyboard_builder(
        [
            [("✅ Заказать", f"entering_date")],
            [("❌ Убрать", f"remove_message")],
        ]
    )
    # TODO: удалять прошлое сообщение либо хотябы убирать из него клавиатуру.
    await store.tg_api.send_media_group(
        chat_id=update.get_chat_id(),
        media_items=[
            {
                "type": "photo",
                "file_id": "AgACAgIAAxkDAAIewmgkTFVQwFE2vyUqMmVUbHQOO6UTAALI7DEbtLQoSWaxos7VuSZ6AQADAgADcwADNgQ",
                "caption": text,
            },
            {
                "type": "photo",
                "file_id": "AgACAgIAAxkDAAIewWgkRhfhhz1IQa6nzL5GIKyNM0QrAAJd9DEbGhkgSRE3-vJU6jNjAQADAgADeAADNgQ",
                # "caption": "Фото по ссылке"
            },
            {
                "type": "photo",
                "file_id": "AgACAgIAAxkDAAIev2gkRUYxl76b6bLhz1jAuqdSLzs-AAJt7DEbtLQoSUHuX48UhUsSAQADAgADeAADNgQ",
                # "caption": "Фото с файла"
            },
        ],
        reply_markup=keyboard,
    )
    # await store.tg_api.edit_message_text(
    #     chat_id=update.get_chat_id(),
    #     message_id=update.get_message_id(),
    #     text=text,
    #     reply_markup=keyboard,
    # )
    keyboard = inline_keyboard_builder(
        [
            [("🔙 Программы", f"choosing_program")],
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.get_chat_id(),
        text="Возврат к выбору",
        reply_markup=keyboard,
    )


async def entering_date(update: "UpdateCallBackQuery", store: "Store", *args):
    # TODO
    text = "Тут будет описанно торговое предложение и переход к оформлению/заполнение анкеты"
    keyboard = inline_keyboard_builder(
        [
            [("📝 Оформить", f"TODO")],
            [("❌ Убрать", f"remove_message")],
        ]
    )

    await store.tg_api.send_message(
        chat_id=update.get_chat_id(),
        text=text,
        reply_markup=keyboard,
    )
