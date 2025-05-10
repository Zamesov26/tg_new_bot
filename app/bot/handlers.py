import re
import typing
from collections.abc import Callable

from app.bot.filters import TextFilter
from app.bot.models import (
    UpdateCallBackQuery,
    UpdateMessage,
    UpdateMyChatMember,
)

if typing.TYPE_CHECKING:
    from app.bot.models import UpdateBase
    from app.tg_api.models import Update


class BaseHandler:
    def check(
        self, update: "Update", *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        pass


class TextHandler(BaseHandler):
    def __init__(self, callback: Callable, text_filter: Callable | None = None):
        self.callback = callback
        if not text_filter:
            text_filter = TextFilter()
        self.text_filter = text_filter

    def check(
        self, update: "Update", *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        if update.message and self.text_filter(update):
            return UpdateMessage(update), self.callback
        return None


class CommandHandler(TextHandler):
    def __init__(self, callback: Callable, command: str, *args):
        super().__init__(callback)
        # TODO потом тоже заменить на ормальный фильтр
        self.text_filter = (
            lambda x: x.message.text[1:].lower().startswith(command)
        )


class AddedToChatHandler(BaseHandler):
    def __init__(self, callback: Callable, *args, **kwargs):
        self.callback = callback

    def check(
        self, update: "Update", *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        if (
            update.my_chat_member
            and update.my_chat_member.old_chat_member.status
            in ("left", "kicked")
            and update.my_chat_member.new_chat_member.status == "member"
        ):
            return UpdateMyChatMember(update), self.callback

        return None


class CallbackQueryHander(BaseHandler):
    def __init__(self, callback: Callable, pattern: str = ""):
        self.callback = callback
        self.pattern = pattern

    def check(
        self, update: "Update", *args, **kwargs
    ) -> tuple["UpdateCallBackQuery", Callable] | None:
        if (
            update.callback_query
            and update.callback_query.data
            and re.match(self.pattern, update.callback_query.data)
        ):
            return UpdateCallBackQuery(update), self.callback
        return None


class ConversationEndError(Exception):
    pass


class ConversationHander:
    def __init__(
        self,
        entry_points: list[BaseHandler],
        states: dict[int | str, list[BaseHandler]],
        fallbacks: list[BaseHandler] | None = None,
    ):
        self.entry_points = entry_points
        self.fallbacks = fallbacks
        self.states = states

    def check(
        self, update: "Update", state: int | str, *args, **kwargs
    ) -> tuple["UpdateBase", Callable] | None:
        if state is None:
            for handler in self.entry_points:
                if res := handler.check(update):
                    return res
            return None
        for handler in self.states.get(state, []):
            if foo := handler.check(update):
                return foo
        if self.fallbacks:
            for handler in self.fallbacks:
                if foo := handler.check(update):
                    return foo
        return None

    @classmethod
    def end(cls):
        raise ConversationEndError
