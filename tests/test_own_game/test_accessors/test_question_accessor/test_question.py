import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select

from app.own_game.models import Category, Question
from app.store import Store
from tests.utils import question_to_dict, questions_to_dict


class TestQuestionsAccessor:
    QUESTION_TITLE_EXAMPLE = "title"

    async def test_table_exists(self, inspect_list_tables: list[str]):
        assert "questions" in inspect_list_tables

    async def test_get_question_by_title(
        self, store: Store, question_1: Question
    ):
        question = await store.question.get_question_by_title(question_1.title)
        assert question_to_dict(question) == {
            "id": question.id,
            "title": question.title,
            "category_id": question.category_id,
            "answer": question.answer,
        }

    async def test_get_list_questions(
        self, store: Store, question_1: Question, question_2: Question
    ):
        questions = await store.question.list_questions()
        assert questions_to_dict(questions) == [
            {
                "id": question_1.id,
                "title": question_1.title,
                "category_id": question_1.category_id,
                "answer": question_1.answer,
            },
            {
                "id": question_2.id,
                "title": question_2.title,
                "category_id": question_2.category_id,
                "answer": question_2.answer,
            },
        ]

    async def test_create_question(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        store: Store,
        category_1: Category,
    ):
        question = await store.question.create_question(
            self.QUESTION_TITLE_EXAMPLE, "Ok", category_1.id
        )
        assert isinstance(question, Question)

        async with db_sessionmaker() as session:
            db_questions = await session.scalars(select(Question))

        db_questions = list(db_questions.all())

        assert questions_to_dict(db_questions) == [
            {
                "id": question.id,
                "title": question.title,
                "category_id": question.category_id,
                "answer": question.answer,
            }
        ]

    async def test_23503_error_when_create_question_without_theme(
        self, store: Store
    ) -> None:
        with pytest.raises(IntegrityError) as exc_info:
            await store.question.create_question(
                self.QUESTION_TITLE_EXAMPLE,
                "Ok",
                1,
            )

        assert exc_info.value.orig.pgcode == "23503"

    async def test_23502_error_when_create_question_with_bad_theme_id(
        self, store: Store
    ):
        with pytest.raises(IntegrityError) as exc_info:
            await store.question.create_question(
                self.QUESTION_TITLE_EXAMPLE, "Ok", None
            )

        assert exc_info.value.orig.pgcode == "23502"

    async def test_23503_error_when_create_question_with_duplicated_title(
        self,
        store: Store,
        question_1: Question,
    ):
        with pytest.raises(IntegrityError) as exc_info:
            await store.question.create_question(
                question_1.title,
                "Ok",
                question_1.category_id,
            )

        assert exc_info.value.orig.pgcode == "23505"
