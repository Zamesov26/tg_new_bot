from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.database.sqlalchemy_base import BaseModel

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application") -> None:
        self.app = app

        self.engine: AsyncEngine
        self._db: type[DeclarativeBase] = BaseModel
        self.session: async_sessionmaker[AsyncSession]

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        self.app.logger.info("start database accessor")
        self.engine = create_async_engine(self.app.config.database.url())
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        await self.engine.dispose()
        self.app.logger.info("stopped database accessor")
