import asyncio
import typing
from asyncio import Queue, Task
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

if typing.TYPE_CHECKING:
    from app.tg_api.models import Update
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.handlers = []
        self.logger = getLogger("BotManager")
        self._queue_updates = Queue()
        self.running = False
        self.life_task: Task

    def _done_callback(self, result):
        if result.exception():
            self.logger.exception(
                "task handler stopped with exception",
                exc_info=result.exception(),
            )

    async def life_loop(self):
        while self.running:
            update = await self._queue_updates.get()
            print(update)
            update_task = asyncio.create_task(self.handle_updates(update))
            update_task.add_done_callback(self._done_callback)

    async def start(self, *args, **kwargs) -> None:
        self.logger.info("start loop")
        self.running = True
        self.life_task = asyncio.create_task(self.life_loop())

    async def stop(self, *args, **kwargs) -> None:
        self.running = False
        self.life_task.cancel()

    async def add_update(self, update: "Update"):
        await self._queue_updates.put(update)

    async def handle_updates(self, update: "Update"):
        db_session: AsyncSession = self.app.database.session()
        async with db_session.begin():
            state = None
            for handler in self.handlers:
                res = handler.check(update, state=state)
                if res:
                    update_object, callback = res
                    self.logger.info(
                        f"run update handler {update.update_id}, state={state}"
                    )
                    res = await callback(
                        update_object, self.app.store, db_session
                    )
                    if res and not res["ok"]:
                        self.logger.warning(res)
                    break
