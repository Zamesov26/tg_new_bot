from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class Chat(BaseModel):
    id: int
    chat_type: str = Field(alias="type")


class InaccessibleMessage(BaseModel):
    message_id: int
    chat: Chat
    date: int

    @field_validator("date")
    @classmethod
    def date_should_be_equal_zero(cls, v: int) -> int:
        if v != 0:
            raise ValueError
        return v


class InlineKeyboardButton(BaseModel):
    text: str
    # url: Optional[str] = None
    callback_data: str | None = None


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: list[list[InlineKeyboardButton]] | None


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: bool = True


# хотелось бы добавить каике-то методы для работы с сообщениями
# replay_message
# delete_message
# edit_message
# как вариант создать базовый класс от которого уснаследовать
class Message(BaseModel):
    message_id: int
    date: int  # всегда положительное
    chat: Chat
    text: str | None = None
    caption: str | None = None
    sender_chat: Chat | None = None
    from_user: User | None = Field(alias="from", default=None)
    reply_markup: InlineKeyboardMarkup | None = None


class CallbackQuery(BaseModel):
    id: str
    from_user: User = Field(alias="from")
    message: Message
    inline_message_id: str | None = None
    data: str


class ChatMemberMember(BaseModel):
    status: str
    user: User


class ChatMember(BaseModel):
    # под ним можно понимать 6 вариантов классов
    # ChatMemberMember
    pass


class ChatMemberUpdated(BaseModel):
    chat: Chat
    from_user: User = Field(alias="from")
    date: int
    old_chat_member: ChatMemberMember  # ChatMember
    new_chat_member: ChatMemberMember  # ChatMember
    # invite_link


class Update(BaseModel):
    message: Message | None = None
    callback_query: CallbackQuery | None = None
    my_chat_member: ChatMemberUpdated | None = None

    update_id: int
