import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="dev-queue")
channel.basic_publish(exchange="", routing_key="dev-queue", body="Hello World!")
print(" [x] Sent 'Hello World!'")
connection.close()
