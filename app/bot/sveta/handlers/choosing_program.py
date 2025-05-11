from app.bot.models import UpdateCallBackQuery
from app.bot.utils import inline_keyboard_builder
from app.store import Store


async def programs(update: "UpdateCallBackQuery", store: "Store", *args):
    text = (
        "🫧 Бабл шоу — $250\n"
        "30–40 минут волшебства с пузырями, дымом, огнём и погружением в пузырь 💫\n\n"
        "🫧+🎭 Комбо-программа — $380\n"
        "1,5 часа: бабл шоу + активные игры, танцы и реквизит 🥳\n\n"
        "🧸 Аниматор — $200\n"
        "40 минут весёлых игр с любимым персонажем 🎈\n\n"
        "🎁 Акции:\n"
        "- 2 персонажа за $200\n"
        "и другие..."
    )
    keyboard = inline_keyboard_builder(
        [
            [
                ("🫧 Бабл шоу", "viewing_details:buble"),
                ("🫧+🎭 Комбо", "viewing_details:combo"),
            ],
            [
                ("🧸 Аниматор", "viewing_details:aminator"),
                ("🎁 Акции", "promo"),
            ],
            [("🔙 Назад", "main_menu")],
        ]
    )
    await store.tg_api.edit_message_text(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
        text=text,
        reply_markup=keyboard,
    )


async def viewing_details(update: "UpdateCallBackQuery", store: "Store", *args):
    _, program = update.callback_query.data.split(":")
    text = (
        f"Показываем описание {program}, оно не будет обновляться, чтобы клиент мог полистать историю сообщений\n"
        "Еще нужно подумать над добавлением фотографий"
    )
    keyboard = inline_keyboard_builder(
        [
            [("✅ Заказать", f"entering_date")],
            [("❌ Убрать", f"remove_message")],
        ]
    )
    await store.tg_api.edit_message_text(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
        text=text,
        reply_markup=keyboard,
    )
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
