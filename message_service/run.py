import asyncio
import json

import aio_pika
from accessor import TgApiAccessor


async def worker(queue_name, callback):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body)
                    await callback(**data)


async def main():
    tg_accessor = TgApiAccessor()
    tg_accessor.connect()
    delete_task = asyncio.create_task(
        worker("delete_message_queue", tg_accessor.delete_message)
    )
    update_markup = asyncio.create_task(
        worker(
            "edit_message_reply_markup_queue",
            tg_accessor.edit_message_reply_markup,
        )
    )

    await asyncio.gather(delete_task, update_markup)


if __name__ == "__main__":
    asyncio.run(main())
