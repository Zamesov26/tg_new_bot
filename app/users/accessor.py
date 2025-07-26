from aiocache import SimpleMemoryCache, cached
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_accessor import BaseAccessor
from app.tg_api.models import User
from app.users.models import User as UserModel


class UserAccessor(BaseAccessor):
    async def get_by_id(
        self, db_session: AsyncSession, user_id: int
    ) -> UserModel:
        stmt = (
            select(UserModel)
            .where(UserModel.tg_id == user_id)
            .with_for_update()
        )
        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_tg_id(
        self, db_session: AsyncSession, tg_id: int
    ) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.tg_id == tg_id)
        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, db_session: AsyncSession) -> list[UserModel]:
        stms = select(UserModel)
        res = await db_session.execute(stms)
        return list(res.scalars().all())

    @cached(ttl=60 * 5, cache=SimpleMemoryCache)
    async def get_or_create(
        self, db_session: AsyncSession, tg_user: User
    ) -> tuple[UserModel, bool]:
        user = await self.get_by_id(db_session, tg_user.tg_id)
        if user:
            return user, False

        user = UserModel(
            tg_id=tg_user.tg_id,
            user_name=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            langue_code=tg_user.language_code,
        )
        db_session.add(user)

        return user, True
