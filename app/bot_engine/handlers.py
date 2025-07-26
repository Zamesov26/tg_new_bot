import re
import typing
from collections.abc import Callable

from app.bot_engine.filters import TextFilter
from app.bot_engine.models import (
    UpdateCallBackQuery,
    UpdateMessage,
    UpdateMyChatMember,
)

if typing.TYPE_CHECKING:
    from app.bot_engine.models import UpdateBase
    from app.bot_engine.update_context import Context


class BaseHandler:
    async def check(
        self, ctx, *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        pass


class TextHandler(BaseHandler):
    def __init__(self, callback: Callable, text_filter: Callable | None = None):
        self.callback = callback
        if not text_filter:
            text_filter = TextFilter()
        self.text_filter = text_filter

    async def check(
        self, ctx, *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        if ctx.update.message and self.text_filter(ctx.update):
            return UpdateMessage(ctx.update), self.callback
        return None


class CommandHandler(TextHandler):
    def __init__(self, callback: Callable, command: str, *args, **kwargs):
        super().__init__(callback)
        # TODO заменить на нормальный фильтр
        self.text_filter = (
            lambda x: x.message.text[1:].lower().startswith(command)
        )


class AddedToChatHandler(BaseHandler):
    def __init__(self, callback: Callable, *args, **kwargs):
        self.callback = callback

    async def check(
        self, ctx, *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        if ctx.update.my_chat_member:
            if (
                ctx.update.my_chat_member
                and ctx.update.my_chat_member.old_chat_member.status
                in ("left", "kicked")
                and ctx.update.my_chat_member.new_chat_member.status == "member"
            ):
                return UpdateMyChatMember(ctx.update), self.callback
            else:
                ctx.logger.warning(
                    "С пользователем произошло не описанное событие"
                )

        return None


class CallbackQueryHandler(BaseHandler):
    def __init__(self, callback: Callable, pattern: str = "", *args, **kwargs):
        self.callback = callback
        self.pattern = pattern

    async def check(
        self, ctx, *args, **kwargs
    ) -> tuple["UpdateCallBackQuery", Callable] | None:
        if (
            ctx.update.callback_query
            and ctx.update.callback_query.data
            and re.match(self.pattern, ctx.update.callback_query.data)
        ):
            return UpdateCallBackQuery(ctx.update), self.callback
        return None


class ConversationEndError(Exception):
    pass


# TODO как будто может быть како-то унииклаьный id и при завершении отправлять уведомление
# TODO когда завершается конверсэйшн, можно вызывать какой-то callback
class ConversationHandler:
    def __init__(
        self,
        entry_points: list[BaseHandler],
        states: dict[int | str, list[BaseHandler]],
        fallbacks: list[BaseHandler] | None = None,
    ):
        self.entry_points = entry_points
        self.states = states
        self.fallbacks = fallbacks

    async def check(
        self, ctx: "Context", *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        # TODO дергать fsm из контекста заполнение и хранение в нем будет более удобно
        fsm = await ctx.store.fsm.get_fsm(ctx)
        if fsm:
            ctx.fsm_state = fsm.state
            ctx.fsm_data = fsm.data
        if fsm is None or ctx.fsm_state is None:
            for handler in self.entry_points:
                if res := await handler.check(ctx):
                    return res
            if self.fallbacks:
                for handler in self.fallbacks:
                    if foo := await handler.check(ctx):
                        return foo

        for handler in self.states.get(fsm.state, []):
            if foo := await handler.check(ctx):
                return foo
        return None

    @classmethod
    def end(cls):
        # TODO: Вызов callback
        raise ConversationEndError
