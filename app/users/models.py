from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy_base import BaseModel


class UserState(str, Enum):
    ACTIVE = "active"
    KICKED = "kicked"
    BANNED = "banned"


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(10))
    state: Mapped[UserState] = mapped_column(
        SQLEnum(UserState, name="user_state_enum"), nullable=False
    )
