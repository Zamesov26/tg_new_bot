from app.bot_engine.models import UpdateCallBackQuery
from app.bot_engine.utils import inline_keyboard_builder
from app.store import Store


async def feedback_input(update: UpdateCallBackQuery, store: Store, *args):
    text = "TODO: нужно подумтаь, что именно мы хотим, просто взять телефон, предложить контакты и т.д."
    keyboard = inline_keyboard_builder(
        [
            [("🔙 Меню", f"main_menu")],
        ]
    )
    await store.tg_api.edit_message_text(
        chat_id=update.get_chat_id(),
        message_id=update.get_message_id(),
        text=text,
        reply_markup=keyboard,
    )
