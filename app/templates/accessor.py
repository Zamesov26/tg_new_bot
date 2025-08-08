from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_accessor import BaseAccessor
from app.templates.models import Template


class TemplateAccessor(BaseAccessor):
    async def get_template(self, db_session: AsyncSession, command: str, model_name: str) -> Template:
        stmt = select(Template).where(Template.model==model_name, Template.type == command)
        return await db_session.scalar(stmt)