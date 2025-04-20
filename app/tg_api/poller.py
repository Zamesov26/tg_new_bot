import asyncio
from asyncio import Future, Task
from logging import getLogger

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Task
        self.logger = getLogger("TgAPIPoller")

    def _done_callback(self, result: Future):
        if result.exception():
            self.logger.exception(
                "poller stopped with exception", exc_info=result.exception()
            )
        if self.is_running:
            self.start()

    def start(self):
        self.logger.info("start")
        self.is_running = True

        self.poll_task = asyncio.create_task(self.poll())
        self.poll_task.add_done_callback(self._done_callback)

    async def stop(self):
        self.logger.info("stop")
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            await self.store.tg_api.poll()
