from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.bot.game_bot.constants import States
from app.database.sqlalchemy_base import BaseModel
from app.own_game.models.questions import Question
from app.own_game.models.users import User


class Game(BaseModel):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT)
    is_active: Mapped[bool] = mapped_column(default=True)
    state: Mapped[int] = mapped_column(default=States.PREPARING)
    active_user_id: Mapped[Optional["User"]] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    responding_user_id: Mapped[Optional["User"]] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    active_question_id: Mapped[Optional["Question"]] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )

    players: Mapped[list["Player"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )
    question_assocciation: Mapped[list["QuestionsToGame"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )
    questions: AssociationProxy[list["Question"]] = association_proxy(
        "question_assocciation", "question"
    )
    responding_user: Mapped["User"] = relationship(
        "User",
        primaryjoin=User.id == responding_user_id,
        foreign_keys=[responding_user_id],
    )
    active_user: Mapped["User"] = relationship(
        "User",
        primaryjoin=User.id == active_user_id,
        foreign_keys=[active_user_id],
    )
    active_question: Mapped["Question"] = relationship("Question")


class Player(BaseModel):
    __tablename__ = "players"
    __table_args__ = (
        UniqueConstraint("user_id", "game_id", name="_user_id_game_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped["User"] = mapped_column(ForeignKey("users.id"))
    points: Mapped[int] = mapped_column(default=0)
    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE")
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    game: Mapped["Game"] = relationship(back_populates="players")
    user: Mapped["User"] = relationship(backref="players")


class QuestionsToGame(BaseModel):
    __tablename__ = "questions_games"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped["Question"] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    game_id: Mapped["Game"] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE")
    )
    price: Mapped[int] = mapped_column(default=0)
    is_available: Mapped[bool] = mapped_column(default=True)
    end_time: Mapped[int | None]

    game: Mapped["Game"] = relationship(back_populates="question_assocciation")
    question: Mapped["Question"] = relationship(
        "Question", backref="game_question"
    )
