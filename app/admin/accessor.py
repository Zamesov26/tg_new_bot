from typing import TYPE_CHECKING

from sqlalchemy import select

from app.admin.models import AdminModel, hash_password
from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.session_maker = app.database.session

        admin = await self.get_by_email(app.config.admin.email)
        if not admin:
            await self.create_admin(
                app.config.admin.email, app.config.admin.password
            )

    async def get_by_email(self, email: str) -> AdminModel | None:
        async with self.session_maker() as session:
            stmt = select(AdminModel).where(AdminModel.email == email)
            cur = await session.execute(stmt)
            return cur.scalar_one_or_none()

    async def create_admin(self, email: str, password: str) -> AdminModel:
        async with self.session_maker() as session:
            new_admin = AdminModel(
                email=email, password=hash_password(password)
            )
            session.add(new_admin)
            await session.commit()
            await session.refresh(new_admin)
            return new_admin
