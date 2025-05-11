from app.bot.models import UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.store import Store


async def viewing_faq(update: "UpdateMessage", store: "Store", *args):
    text = (
        "❓ Что входит в бабл шоу?\n"
        "💬 Шоу длится 30–40 минут и включает трюки с гигантскими пузырями, пузырями с дымом и огнём, миллион мыльных пузырей, а также погружение ребёнка в пузырь 🫧✨\n\n"
        "❓ Можно ли проводить шоу на улице?\n"
        "💬 Да, но в зависимости от погоды. На улице мы делаем более динамичную версию шоу без сложных трюков — много пузырей, весёлые ракетки, игры с детьми 🌬️🎉"
    )
    keyboard = inline_keyboard_builder(
        [
            [("⬅️ Назад", "prev_questions"), ("➡️ Далее", "next_questions")],
            [("🔙 Меню", "main_menu")],
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.get_chat_id(), text=text, reply_markup=keyboard
    )
