from app.bot_engine.update_context import UpdateContext
from app.bot_engine.utils import inline_keyboard_builder


async def feedback_input(ctx: UpdateContext, *args, **kwargs):
    text = "TODO: нужно подумтаь, что именно мы хотим, просто взять телефон, предложить контакты и т.д."
    keyboard = inline_keyboard_builder(
        [
            [("🔙 Меню", f"main_menu")],
        ]
    )
    await ctx.store.tg_api.edit_message_text(
        chat_id=ctx.update.get_chat_id(),
        message_id=ctx.update.get_message_id(),
        text=text,
        reply_markup=keyboard,
    )
