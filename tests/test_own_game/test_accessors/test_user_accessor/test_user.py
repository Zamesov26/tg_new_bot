from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.own_game.models import User
from app.store.store import Store


class TestGameAccessor:
    async def test_table_exists(self, inspect_list_tables: list[str]):
        assert "users" in inspect_list_tables

    async def test_create_user(
        self, db_sessionmaker: async_sessionmaker[AsyncSession], store: Store
    ) -> None:
        name = "1" * 100
        user = await store.user.create_user(tg_id=1, name=name)

        assert isinstance(user, User)

        async with db_sessionmaker() as session:
            users = list(await session.scalars(select(User)))

        assert len(users) == 1
        assert users[0].id == user.id
        assert users[0].name == name[:10]
