import json
from .connection import get_connection

EXCHANGE_NAME='fresh_milk'

def publish_message(data):
    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout',
        durable=True
    )

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key='',
        body=json.dumps(data),
    )