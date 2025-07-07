from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.base.base_accessor import BaseAccessor
from app.questionnaire.models import (
    Answer,
    FormInstance,
    Question,
    Questionnaire,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.bot_engine.update_context import Context


class QuestionnaireAccessor(BaseAccessor):
    async def get_questionnaire(
        self, db_session: "AsyncSession", questionnaire_name: str
    ):
        stmt = select(Questionnaire).where(
            Questionnaire.title == questionnaire_name
        )
        questions = await db_session.execute(stmt)
        return questions.scalar_one_or_none()

    async def get_question_ids(
        self, db_session: "AsyncSession", questionnaire_id: int
    ):
        stmt = select(Question.id).where(
            Question.questionnaire_id == questionnaire_id
        )
        questions = await db_session.execute(stmt)
        return questions.scalars()

    async def get_question(self, db_session: "AsyncSession", question_id: int):
        stmt = select(Question).where(Question.id == question_id)
        question = await db_session.execute(stmt)
        return question.scalar()

    async def create_form_instance(
        self, db_session: "AsyncSession", user_id: int, questionare_id: int
    ):
        form_instance = FormInstance(
            user_id=user_id, questionnaire_id=questionare_id
        )
        db_session.add(form_instance)
        await db_session.flush()
        return form_instance

    async def create_answer(
        self,
        ctx: "Context",
        question_id: int,
        form_instance_id: int,
        value: str,
    ):
        stmt = (
            insert(Answer)
            .values(
                question_id=question_id,
                form_instance_id=form_instance_id,
                user_id=ctx.user_id,
                value=value,
            )
            .on_conflict_do_update(
                index_elements=["question_id", "form_instance_id"],
                set_={"value": value},
            )
        )

        await ctx.db_session.execute(stmt)
