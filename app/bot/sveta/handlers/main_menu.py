from app.bot.utils import inline_keyboard_builder


async def main_menu(update: "UpdateMessage", store: "Store", *args):
    text = (
        "Привет 🤗\n"
        "Добро пожаловать в Wonderland — волшебный мир шоу пузырей и весёлых аниматоров!\n"
        "Чем могу помочь?"
    )
    keyboard = inline_keyboard_builder(
        [
            [("🎭 Программы и заказ", f"choosing_program")],
            [("📸 Каталог персонажей", f"TODO")],
            [("❓ Частые вопросы", f"TODO")],
            [("📞 Связаться с нами", f"TODO")],
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.message.chat.id, text=text, reply_markup=keyboard
    )


