from app.bot.models import UpdateCallBackQuery, UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.store import Store


async def main_menu(
    update: UpdateCallBackQuery | UpdateMessage, store: "Store", *args
):
    text = (
        "Добро пожаловать в Wonderland — волшебный мир шоу пузырей и весёлых аниматоров!\n"
        "Чем могу помочь?"
    )
    keyboard = inline_keyboard_builder(
        [
            [("🎭 Программы и заказ", "choosing_program")],
            [("📸 Каталог персонажей", "TODO")],
            [("❓ Частые вопросы", "viewing_faq")],
            [("📞 Связаться с нами", "feedback_input")],
        ]
    )
    if isinstance(update, UpdateCallBackQuery):
        await store.tg_api.edit_message_text(
            chat_id=update.get_chat_id(),
            message_id=update.get_message_id(),
            text=text,
            reply_markup=keyboard,
        )
    else:
        await store.tg_api.send_message(
            chat_id=update.get_chat_id(),
            text=text,
            reply_markup=keyboard,
        )
