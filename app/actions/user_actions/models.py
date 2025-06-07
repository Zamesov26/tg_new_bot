from datetime import datetime, UTC
from enum import Enum

from sqlalchemy import ForeignKey, String, Text, Integer, BigInteger, DateTime, BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy_base import BaseModel


class UserAction(BaseModel):
    __tablename__ = "user_actions"

    class Status(Enum):
        UNCONFIRMED = "unconfirmed"
        SUCCESS = "success"
        FAILED = "failed"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BIGINT)

    action_type: Mapped[str] = mapped_column(String(64), nullable=False)
    action_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    status: Mapped[Status] = mapped_column(
        String(11), nullable=False, default=Status.UNCONFIRMED
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
