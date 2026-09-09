import json
from .producer import EXCHANGE_NAME
from .connection import get_connection

def start_consuming(queue_name, callback):
    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout',
        durable=True
    )

    channel.queue_declare(
        queue=queue_name,
        durable=True
    )

    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name,
    )

    def on_message(ch, method, properties, body):
        data = json.loads(body)
        callback(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_message,
        auto_ack=False
    )

    channel.start_consuming()
