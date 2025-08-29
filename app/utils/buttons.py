from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from app.bot_engine.update_context import Context


def additional_buttons(handle: Callable, buttons: list[list[str]]):
    def wrapper(ctx: "Context", *args, **kwargs):
        ctx.additional_keyboard = [buttons]
        return handle(ctx, *args, **kwargs)
    
    return wrapper