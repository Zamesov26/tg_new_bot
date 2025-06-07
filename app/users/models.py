import enum
from enum import Enum

from sqlalchemy import VARCHAR, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy_base import BaseModel


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    RESTRICTED = "restricted"


class UserState(str, Enum):
    ACTIVE = "active"
    KICKED = "kicked"
    BANNED = "banned"


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(32))
    first_name: Mapped[str] = mapped_column(VARCHAR(64))
    last_name: Mapped[str] = mapped_column(VARCHAR(64), nullable=True)
    langue_code: Mapped[str] = mapped_column(VARCHAR(10), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        String(20),
        nullable=True,
        default=UserRole.USER.value,
        server_default=UserRole.USER.value,
    )
    state: Mapped[UserState] = mapped_column(
        String(20),
        nullable=True,
        default=UserState.ACTIVE.value,
        server_default=UserState.ACTIVE.value,
    )
