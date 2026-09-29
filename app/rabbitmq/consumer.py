import json
import logging

from .connection import get_connection
from .producer import EXCHANGE_NAME, SMS_QUEUE

logger = logging.getLogger(__name__)


def start_consuming(queue_name=SMS_QUEUE, callback=None):
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

    channel.basic_qos(prefetch_count=10)

    def on_message(ch, method, properties, body):
        try:
            data = json.loads(body)
            callback(data)
        except Exception:
            logger.exception("Failed processing message from %s", queue_name)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_message,
        auto_ack=False
    )

    channel.start_consuming()
