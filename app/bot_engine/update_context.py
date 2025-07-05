import typing

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.store import Store
    from app.tg_api.models import Update
    from app.users.models import User


class Context:
    store: "Store"
    db_session: "AsyncSession"
    update: "Update"
    event: typing.Union["Update", None] = None
    update_res: dict | None = None
    fsm_state: str | int | None = None
    fsm_data: dict | None = None
    user: typing.Union["User", None]

    def __init__(
        self,
        store: "Store",
        db_session: "AsyncSession",
        update: "Update",
    ):
        self.store = store
        self.db_session = db_session
        self.update = update

    def set_event(self, update: "Update"):
        self.event = update
        self.update_res = None

    @property
    def chat_id(self):
        if self.update.message:
            return self.update.message.chat.id
        elif self.update.callback_query:
            return self.update.callback_query.message.chat.id
        elif self.update.my_chat_member:
            return self.update.my_chat_member.chat.id

        return None

    @property
    def user_id(self):
        if self.update.message:
            return self.update.message.from_user.tg_id
        elif self.update.callback_query:
            return self.update.callback_query.from_user.tg_id
        elif self.update.my_chat_member:
            return self.update.my_chat_member.from_user.tg_id

        return None
