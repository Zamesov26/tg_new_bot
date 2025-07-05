from sqlalchemy import JSON, BigInteger, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy_base import BaseModel


class FSM(BaseModel):
    __tablename__ = "fsm"
    __table_args__ = (
        UniqueConstraint("chat_id", "user_id", name="uq_fsm_chat_user"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=True)
