from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_accessor import BaseAccessor
from app.own_game.models.users import User


class UserAccessor(BaseAccessor):
    async def create_user(
        self, db_session: AsyncSession, tg_id: int, name
    ) -> User:
        user = User(tg_id=tg_id, name=name[:10])
        db_session.add(user)
        await db_session.flush()
        return user

    async def get_by_id(self, db_session: AsyncSession, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        res = await db_session.execute(stmt)
        return res.scalar_one()

    async def get_by_tg_id(
        self, db_session: AsyncSession, tg_id: int
    ) -> User | None:
        stmt = select(User).where(User.tg_id == tg_id)
        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, db_session: AsyncSession) -> list[User]:
        stms = select(User)
        res = await db_session.execute(stms)
        return list(res.scalars().all())
