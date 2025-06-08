from app.bot_engine.update_context import UpdateContext


async def delete_message(ctx: UpdateContext, *args, **kwargs):
    await ctx.store.tg_api.delete_message(
        chat_id=ctx.update.get_chat_id(),
        message_id=ctx.update.get_message_id(),
    )
