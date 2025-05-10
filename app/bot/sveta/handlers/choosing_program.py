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
        "🎁 Акция — 2 персонажа за $200\n"
        "Отлично подойдёт для праздника с большим количеством детей 😍\n"
    )
    keyboard = inline_keyboard_builder(
        [
            [("🫧 Бабл шоу", f"buble"), ("🫧+🎭 Комбо", f"combo")],
            [("🧸 Аниматор", f"aminator"), ("🎁 Акции", f"promo")],
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.callback_query.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
    
async def viewing_details(update: "UpdateCallBackQuery", store: "Store", *args):
    text = (
        "показываем описание"
    )
    keyboard = inline_keyboard_builder(
        [
            [("✅ Заказать", f"entering_date")],
            [("🔙 Назад", f"choosing_program")],
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.callback_query.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


async def entering_date(update: "UpdateCallBackQuery", store: "Store", *args):
    # TODO
    text = "TODO: Еще нудо подумать(дата, время, адрес, сколько детей, доп настройки(персонаж)"
    keyboard = inline_keyboard_builder(
        [
            [("🔙 Назад", f"viewing_details")],
        ]
    )

    await store.tg_api.send_message(
        chat_id=update.callback_query.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
