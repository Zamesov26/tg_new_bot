from datetime import UTC, datetime
from functools import wraps

from app.actions import UserAction
from app.bot_engine.update_context import UpdateContext
from app.tg_api.accessor import TelegramAPIError


def log_user_action(action_type: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx: UpdateContext, *args, **kwargs):
            status = UserAction.Status.SUCCESS
            error_message = None

            try:
                result = await func(ctx, *args, **kwargs)
            except TelegramAPIError:
                status = UserAction.Status.FAILED
                error_message = result
                raise
            finally:
                action = UserAction(
                    user_id=ctx.update.from_user.tg_id,
                    action_type="{}:{}".format(
                        action_type, ctx.update.__class__.__name__
                    ),
                    action_data=ctx.update.get_data(),
                    message_id=ctx.update.get_message_id(),
                    chat_id=ctx.update.get_chat_id(),
                    status=status.value,
                    error_message=error_message,
                )
                ctx.db_session.add(action)

            return result

        return wrapper

    return decorator
