from collections.abc import Iterable

import pytest
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.own_game.models import Category, Question
from app.store import Store
from tests.utils import categories_to_dict, category_to_dict


class TestThemeAccessor:
    async def test_table_exists(self, inspect_list_tables: list[str]):
        assert "categories" in inspect_list_tables

    async def test_success_get_theme_by_id(
        self, store: Store, category_1: Category
    ) -> None:
        category = await store.question.get_category_by_id(category_1.id)
        assert isinstance(category, Category)
        assert category_to_dict(category) == category_to_dict(category_1)

    async def test_success_get_theme_by_title(
        self, store: Store, category_1: Category
    ) -> None:
        category = await store.question.get_category_by_name(category_1.name)
        assert isinstance(category, Category)
        assert category_to_dict(category) == category_to_dict(category_1)

    async def test_success_get_list(
        self, store: Store, category_1: Category
    ) -> None:
        categories_list = await store.question.list_categories()
        assert isinstance(categories_list, Iterable)
        assert categories_to_dict(categories_list) == [
            category_to_dict(category_1)
        ]

    async def test_create_theme(
        self, db_sessionmaker: async_sessionmaker[AsyncSession], store: Store
    ) -> None:
        category = await store.question.create_category("title")
        assert isinstance(category, Category)

        async with db_sessionmaker() as session:
            categories = list(await session.scalars(select(Category)))

        assert len(categories) == 1
        assert categories[0].id == category.id
        assert categories[0].name == category.name

    async def test_create_theme_unique_title_constraint(
        self, store: Store, category_1: Category
    ):
        with pytest.raises(IntegrityError) as exc_info:
            await store.question.create_category(category_1.name)

        assert exc_info.value.orig.pgcode == "23505"

    async def test_check_cascade_delete(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        question_1: Question,
    ):
        async with db_sessionmaker() as session:
            category_id = question_1.category_id
            await session.execute(
                delete(Category).where(Category.id == category_id)
            )
            await session.commit()

            db_questions = await session.scalars(
                select(Question).where(Question.category_id == category_id)
            )

        assert len(db_questions.all()) == 0
