import json
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

import pika

from .connection import amqp_connection

EXCHANGE_NAME = 'fresh_milk'
SMS_QUEUE = 'sms_consumer'
PUBLISH_TIMEOUT = 5

logger = logging.getLogger(__name__)

_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix='amqp-publish')


def publish_message(data):
    body = json.dumps(data)
    last_error = None

    for _ in range(2):
        try:
            with amqp_connection() as connection:
                channel = connection.channel()
                try:
                    channel.confirm_delivery()
                    channel.exchange_declare(
                        exchange=EXCHANGE_NAME,
                        exchange_type='fanout',
                        durable=True
                    )
                    channel.queue_declare(queue=SMS_QUEUE, durable=True)
                    channel.queue_bind(
                        exchange=EXCHANGE_NAME,
                        queue=SMS_QUEUE,
                    )
                    channel.basic_publish(
                        exchange=EXCHANGE_NAME,
                        routing_key='',
                        body=body,
                        mandatory=True,
                    )
                finally:
                    if channel.is_open:
                        channel.close()
            return True
        except pika.exceptions.UnroutableError:
            logger.warning("RabbitMQ dropped message, no queue bound to %s", EXCHANGE_NAME)
            return False
        except pika.exceptions.AMQPError as e:
            last_error = e

    raise last_error


def publish_with_timeout(data, timeout=PUBLISH_TIMEOUT):
    future = _executor.submit(publish_message, data)
    try:
        return future.result(timeout=timeout)
    except FutureTimeout:
        logger.warning("RabbitMQ publish timed out after %ss", timeout)
        return False
    except Exception as e:
        logger.warning("RabbitMQ publish failed: %s", e)
        return False
