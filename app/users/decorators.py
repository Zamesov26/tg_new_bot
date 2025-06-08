from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.bot_engine.update_context import UpdateContext


def with_user(handler):
    @wraps(handler)
    async def wrapper(ctx: UpdateContext, *args, **kwargs):
        user, _ = await ctx.store.user.get_or_create(
            ctx.db_session, ctx.update.from_user
        )
        ctx.user = user
        return await handler(ctx, *args, **kwargs)

    return wrapper
