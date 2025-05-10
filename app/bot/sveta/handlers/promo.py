from app.bot.models import UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.store import Store


async def promo(update: "UpdateMessage", store: "Store", *args):
    text = (
        "🎉 2 персонажа по цене одного — $200?\n"
        "Идеально для больших компаний детей — двойное веселье за ту же цену! 😍\n"
        "(Обычно 1 персонаж — $200, а здесь сразу 2 🎭🎭) 🫧✨\n\n"
        
        "🎉 Праздник до 13:00 — скидка 20%\n"
        "Утренние шоу — это не только отличное начало дня, но и выгоднее! 🌞🎉\n\n"
    )
    keyboard = inline_keyboard_builder(
        [
            [("⬅️ Назад", "prev_questions"), ("➡️ Далее", "next_questions")],
            [("🔙 Меню", "main_menu")]
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.message.chat.id, text=text, reply_markup=keyboard
    )

