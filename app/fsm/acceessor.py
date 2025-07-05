import typing

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.base.base_accessor import BaseAccessor
from app.fsm.models import FSM

if typing.TYPE_CHECKING:
    from app.bot_engine.update_context import Context


class FSMAccessor(BaseAccessor):
    @classmethod
    async def update_fsm(
        cls, ctx: "Context", new_state: str | int, new_data: dict | None = None
    ):
        stmt = (
            insert(FSM)
            .values(
                chat_id=ctx.chat_id,
                user_id=ctx.user_id,
                state=new_state,
                data=new_data,
            )
            .on_conflict_do_update(
                index_elements=["chat_id", "user_id"],
                set_={"state": new_state, "data": new_data},
            )
        )
        result = await ctx.db_session.execute(stmt)
        return result

    @classmethod
    async def get_fsm(cls, ctx: "Context"):
        stmt = select(FSM).where(
            FSM.chat_id == ctx.chat_id, FSM.user_id == ctx.user_id
        )
        res = await ctx.db_session.execute(stmt)
        row = res.scalar_one_or_none()
        if row:
            ctx.fsm = row
        return row
