import pika


def get_connection():
    credentials = pika.PlainCredentials(
        "admin",
        "admin123"
    )

    parameters = pika.ConnectionParameters(
        host="localhost",
        port=5674,
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)