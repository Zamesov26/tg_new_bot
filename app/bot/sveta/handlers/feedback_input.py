from app.bot.utils import inline_keyboard_builder


async def feedback_input(update: "UpdateCallBackQuery", store: "Store", *args):
    text = (
        "TODO: нужно подумтаь, что именно мы хотим, просто взять телефон, предложить контакты и т.д."
    )
    keyboard = inline_keyboard_builder(
        [
            [("🔙 меню", f"main_menu")],
        ]
    )
    await store.tg_api.send_message(
        chat_id=update.callback_query.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )