from functools import wraps

from sqlalchemy import select

from app.bot_engine.update_context import Context
from app.fsm.models import FSM


def with_fsm():
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx: Context, *args, **kwargs):
            if not ctx.fsm_state:
                fsm = (
                    await ctx.db_session.execute(
                        select(FSM).where(
                            FSM.chat_id == ctx.event.get_chat_id(),
                            FSM.user_id == ctx.event.get_user_tg_id(),
                        )
                    )
                ).scalar_one_or_none()
                if fsm:
                    ctx.fsm_state = fsm.state
                    ctx.fsm_data = fsm.data
            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator
