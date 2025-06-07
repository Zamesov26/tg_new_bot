from app.bot_engine.update_context import UpdateContext
from app.bot_engine.utils import inline_keyboard_builder


async def viewing_faq(ctx: UpdateContext, *args):
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
    await ctx.store.tg_api.edit_message_text(
        chat_id=ctx.update.get_chat_id(),
        message_id=ctx.update.get_message_id(),
        text=text,
        reply_markup=keyboard,
    )
