from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_accessor import BaseAccessor
from app.programs.models import Programs


class ProgramAccessor(BaseAccessor):
    async def get_by_id(
        self, db_session: AsyncSession, program_id: int
    ) -> Programs:
        stmt = select(Programs).where(Programs.id == program_id)
        res = await db_session.execute(stmt)
        return res.scalar_one()

    async def get_all(self, db_session: AsyncSession) -> list[Programs]:
        stms = select(Programs).where(Programs.is_active)
        res = await db_session.execute(stms)
        return list(res.scalars().all())
