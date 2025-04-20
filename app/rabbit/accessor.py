import json
import typing
from logging import getLogger

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractRobustConnection,
)

from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class RabbitAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app)
        self.logger = getLogger("RabbitAccessor")
        self.connection: AbstractRobustConnection
        self.channel: AbstractChannel

    async def connect(self, *arg, **kwargs):
        self.logger.info("start")

        self.connection = await aio_pika.connect_robust(
            "amqp://guest:guest@127.0.0.1/"
        )
        self.channel = await self.connection.channel()
        await self.channel.declare_queue("delete_message_queue", durable=True)
        await self.channel.declare_queue(
            "edit_message_reply_markup_queue", durable=True
        )

    async def disconnect(self, *args, **kwargs):
        self.logger.info("close")
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

    async def delete_message(self, chat_id: int, message_id: int):
        body = {"chat_id": chat_id, "message_id": message_id}

        await self.channel.default_exchange.publish(
            aio_pika.Message(body=bytes(json.dumps(body), "utf-8")),
            routing_key="delete_message_queue",
        )

    async def edit_message_reply_markup(self, chat_id, message_id, murkup=None):
        body = {"chat_id": chat_id, "message_id": message_id}
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=bytes(json.dumps(body), "utf-8")),
            routing_key="edit_message_reply_markup_queue",
        )
