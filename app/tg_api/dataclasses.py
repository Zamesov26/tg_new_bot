from dataclasses import dataclass
from enum import Enum


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None


class ChatTypes(Enum):
    pprivate = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"


@dataclass
class Chat:
    id: int
    chat_type: ChatTypes  # type


@dataclass
class InaccessibleMessage:
    message_id: int
    chat: Chat
    date: int  # всегда должно быть 0


@dataclass
class InlineKeyboardButton:
    text: str
    # url: Optional[str]
    callback_data: str | None


@dataclass
class InlineKeyboardMarkup:
    inline_keyboard: list[list[InlineKeyboardButton]]


@dataclass
class Message:
    message_id: int
    chat_id: int
    text: str
    date: int  # всегда положительное
    chat: Chat | None
    sender_chat: Chat | None
    from_user: User | None  # from
    reply_markup: InlineKeyboardMarkup | None


@dataclass
class CallbackQuery:
    id: str
    from_user: User  # парсить надо из from
    message: InaccessibleMessage | Message


@dataclass
class Update:
    message: Message | None = None
    callback_query: CallbackQuery | None = None

    @classmethod
    def from_dict(cls, data: dict):
        update = Update()
        if message := data.get("message"):
            if message["data"] == 0:
                update.message = InaccessibleMessage.from_dict(message)
            else:
                update.message = Message.from_dict(message)
