import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.own_game.models import Category, Question, User
from app.own_game.models.games import Game


@pytest.fixture
async def category_1(
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> Category:
    new_theme = Category(name="Деревья")

    async with db_sessionmaker() as session:
        session.add(new_theme)
        await session.commit()

    return new_theme


@pytest.fixture
async def category_2(
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> Category:
    new_theme = Category(title="Животные")

    async with db_sessionmaker() as session:
        session.add(new_theme)
        await session.commit()

    return new_theme


@pytest.fixture
async def question_1(
    db_sessionmaker: async_sessionmaker[AsyncSession], category_1: Category
) -> Question:
    question = Question(
        title="how are you?",
        answer="Ok",
        category_id=category_1.id,
    )

    async with db_sessionmaker() as session:
        session.add(question)
        await session.commit()

    return question


@pytest.fixture
async def question_2(db_sessionmaker, category_1: Category) -> Question:
    question = Question(
        title="are you doing fine?",
        answer="yes",
        category_id=category_1.id,
    )

    async with db_sessionmaker() as session:
        session.add(question)
        await session.commit()

    return question


@pytest.fixture
async def user_1(db_sessionmaker) -> User:
    user = User(tg_id=11, name="user_1")
    async with db_sessionmaker() as session:
        session.add(user)
        await session.commit()

    return user


@pytest.fixture
async def user_2(db_sessionmaker) -> User:
    user = User(tg_id=12, name="user_2")
    async with db_sessionmaker() as session:
        session.add(user)
        await session.commit()

    return user


@pytest.fixture
async def game_1(db_sessionmaker) -> Game:
    game = Game(chat_id=1)
    async with db_sessionmaker() as session:
        session.add(game)
        await session.commit()

    return game
