import typing

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.store import Store
    from app.tg_api.models import Update
    from app.users.models import User


class UpdateContext:
    store: "Store"
    db_session: "AsyncSession"
    update: typing.Union["Update", None] = None
    update_res: dict | None = None
    state: str | int | None
    user: typing.Union["User", None]

    def __init__(
        self,
        store: "Store",
        db_session: "AsyncSession",
    ):
        self.store = store
        self.db_session = db_session

    def set_update(self, update: "Update"):
        self.update = update
        self.update_res = None
