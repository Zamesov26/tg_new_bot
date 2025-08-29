import typing

from aiocache import SimpleMemoryCache, cached
from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.medias.models import Media

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MediaAccessor(BaseAccessor):
    @cached(ttl=60 * 5, cache=SimpleMemoryCache)
    async def get_by_file_path(
        self, db_session: "AsyncSession", path: str
    ) -> Media:
        stmt = select(Media).where(Media.file_path.like(path))
        return await db_session.scalar(stmt)
