import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="dev-queue", durable=True)

message = " ".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange="",
    routing_key="dev-queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)
print(f" [x] Sent {message}")
connection.close()
