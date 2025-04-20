from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from app.base.base_accessor import BaseAccessor
from app.own_game.models import Category, Question
from questions_utils import load_questions


class QuestionAccessor(BaseAccessor):
    async def connect(self, app):
        categories = await self.list_categories()
        if categories:
            return
        question_data = load_questions()
        async with self.app.database.session() as session:
            for theme_name in question_data:
                category = Category(name=theme_name)
                for question in question_data[theme_name]:
                    category.questions.append(
                        Question(
                            title=question["question"],
                            answer=question["answer"],
                        )
                    )
                session.add(category)
            await session.commit()

    async def create_category(self, category_name: str):
        async with self.app.database.session() as session:
            category = Category(name=category_name)
            session.add(category)
            await session.commit()
            return category

    async def get_category_by_id(
        self, db_session: AsyncSession, category_id
    ) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_category_by_name(self, name) -> Category | None:
        async with self.app.database.session() as session:
            stmt = select(Category).where(Category.name == name)
            res = await session.execute(stmt)
            return res.scalar()

    async def list_categories(self) -> list[Category]:
        async with self.app.database.session() as session:
            stmt = select(Category)
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def create_question(self, title, answer, category_id) -> Question:
        async with self.app.database.session() as session:
            question = Question(
                title=title, answer=answer, category_id=category_id
            )
            session.add(question)
            await session.commit()
            return question

    async def get_queestion_by_id(
        self, db_session: AsyncSession, question_id
    ) -> Question:
        stmt = select(Question).where(Question.id == question_id)
        res = await db_session.execute(stmt)
        return res.scalar_one()

    async def get_question_by_title(self, title) -> Question | None:
        async with self.app.database.session() as session:
            stmt = select(Question).where(Question.title == title)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def list_questions(
        self, db_session, category_id: int
    ) -> list[Question]:
        stmt = select(Question).where(Question.category_id == category_id)
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    async def get_random_categoris(
        self, db_session: AsyncSession, theme_cnt=6
    ) -> list[Category]:
        stmt_themes = select(Category).order_by(func.random()).limit(theme_cnt)
        res = await db_session.execute(stmt_themes)
        return list(res.scalars().all())

    async def get_random_question_for_category(
        self, db_session: AsyncSession, category_id: int, question_cnt: int = 3
    ) -> list[Question]:
        stmt_themes = (
            select(Question)
            .where(Question.category_id == category_id)
            .order_by(func.random())
            .limit(question_cnt)
        )
        res = await db_session.execute(stmt_themes)
        return list(res.scalars().all())
