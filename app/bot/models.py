import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from app.tg_api.models import (CallbackQuery, ChatMemberUpdated, Message,
                                   Update)


class UpdateBase(ABC):
    @abstractmethod
    def __init__(self, update: "Update"):
        pass

    @abstractmethod
    def get_chat_id(self):
        pass


class UpdateCallBackQuery(UpdateBase):
    def __init__(self, update: "Update"):
        if not update.callback_query:
            raise TypeError("callback_query field is None")
        self.callback_query: CallbackQuery = update.callback_query

    def get_chat_id(self):
        return self.callback_query.message.chat.id


class UpdateMyChatMember(UpdateBase):
    def __init__(self, update: "Update"):
        if not update.my_chat_member:
            raise TypeError("my_chat_member field is None")
        self.my_chat_member: ChatMemberUpdated = update.my_chat_member

    def get_chat_id(self):
        return self.my_chat_member.chat.id


class UpdateMessage(UpdateBase):
    def __init__(self, update: "Update"):
        if not update.message:
            raise TypeError("message field is None")
        self.message: Message = update.message

    def get_chat_id(self):
        return self.message.chat.id
