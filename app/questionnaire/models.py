from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.sqlalchemy_base import BaseModel


class Questionnaire(BaseModel):
    __tablename__ = "questionnaire"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    instances: Mapped[list["FormInstance"]] = relationship(
        back_populates="questionnaire"
    )


class Question(BaseModel):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey("questionnaire.id")
    )
    text: Mapped[str] = mapped_column(String)
    function_name: Mapped[str | None] = mapped_column(String, nullable=True)


class Answer(BaseModel):
    __tablename__ = "answer"
    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "form_instance_id",
            name="uq_answer_question_forminst",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    value: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    form_instance_id: Mapped[UUID] = mapped_column(
        ForeignKey("form_instance.id")
    )

    form_instance: Mapped["FormInstance"] = relationship(
        back_populates="answers"
    )


class FormInstance(BaseModel):
    __tablename__ = "form_instance"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger)
    questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey("questionnaire.id")
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    questionnaire: Mapped["Questionnaire"] = relationship(
        back_populates="instances"
    )
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="form_instance"
    )
