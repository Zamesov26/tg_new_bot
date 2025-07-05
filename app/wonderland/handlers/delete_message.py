from app.bot_engine.update_context import Context


async def delete_message(ctx: Context, *args, **kwargs):
    await ctx.store.tg_api.delete_message(
        chat_id=ctx.event.get_chat_id(),
        message_id=ctx.event.get_message_id(),
    )
