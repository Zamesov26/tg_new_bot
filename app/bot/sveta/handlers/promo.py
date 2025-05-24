from app.bot.models import UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.store import Store


async def promo(update: "UpdateMessage", store: "Store", *args):
    text = (
        "🎉 2 персонажа по цене одного — $200? действует до: 11.02.2024\n"
        "Идеально для больших компаний детей — двойное веселье за ту же цену! 😍\n"
        "(Обычно 1 персонаж — $200, а здесь сразу 2 🎭🎭) 🫧✨\n\n"
        "🎉 Праздник до 13:00 — скидка 20%\n"
        "Утренние шоу — это не только отличное начало дня, но и выгоднее! 🌞🎉\n\n"
    )
    keyboard = inline_keyboard_builder(
        [
            # [("⬅️ Назад", "TODO"), ("➡️ Далее", "TODO")],
            [("🔙 Меню", "main_menu")],
        ]
    )
    return await store.tg_api.edit_message_media(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
        caption=text,
        file_id="AgACAgIAAxkDAAIewmgkTFVQwFE2vyUqMmVUbHQOO6UTAALI7DEbtLQoSWaxos7VuSZ6AQADAgADcwADNgQ",
        file_path="images/promo.png",
        reply_markup=keyboard,
    )
