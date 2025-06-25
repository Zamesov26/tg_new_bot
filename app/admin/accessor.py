from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_accessor import BaseAccessor
from app.users.models import User


class AdminAccessor(BaseAccessor):
    async def get_all(self, db_session: AsyncSession) -> list[User]:
        stmt = select(User).where(User.role == User.UserRole.ADMIN.value)
        res = await db_session.execute(stmt)
        return list(res.scalars().all())
