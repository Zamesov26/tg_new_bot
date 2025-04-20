import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from app.tg_api.models import (
        CallbackQuery,
        ChatMemberUpdated,
        Message,
        Update,
    )


class UpdateBase(ABC):
    @abstractmethod
    def __init__(self, update: "Update"):
        pass


class UpdateCallBackQuery(UpdateBase):
    def __init__(self, update: "Update"):
        if not update.callback_query:
            raise TypeError("callback_query field is None")
        self.callback_query: CallbackQuery = update.callback_query


class UpdateMyChatMember(UpdateBase):
    def __init__(self, update: "Update"):
        if not update.my_chat_member:
            raise TypeError("my_chat_member field is None")
        self.my_chat_member: ChatMemberUpdated = update.my_chat_member


class UpdateMessage(UpdateBase):
    def __init__(self, update: "Update"):
        if not update.message:
            raise TypeError("message field is None")
        self.message: Message = update.message

    # def answer_text(self, text, m)
