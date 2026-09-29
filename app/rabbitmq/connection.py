import os
import threading
from contextlib import contextmanager

import pika


_lock = threading.Lock()
_connection = None


def _parameters():
    url = os.getenv("RABBITMQ_URL")
    params = pika.URLParameters(url)
    params.socket_timeout = 10
    params.stack_timeout = 15
    params.blocked_connection_timeout = 10
    params.connection_attempts = 3
    params.retry_delay = 2
    params.heartbeat = 30
    return params


def _new_connection():
    return pika.BlockingConnection(_parameters())


def get_connection():
    """Dedicated connection for standalone consumer processes."""
    return _new_connection()


@contextmanager
def amqp_connection():
    """Serialize AMQP access and reuse a single connection.

    pika's BlockingConnection is not thread-safe, so the lock is held for
    the whole block. If the block fails the connection is dropped so the
    next call starts from a fresh one.
    """
    global _connection

    with _lock:
        try:
            if _connection is None or not _connection.is_open:
                _connection = _new_connection()
            yield _connection
        except BaseException:
            try:
                if _connection is not None and _connection.is_open:
                    _connection.close()
            except Exception:
                pass
            _connection = None
            raise


def close_connection():
    global _connection

    with _lock:
        if _connection is not None and _connection.is_open:
            try:
                _connection.close()
            except Exception:
                pass
        _connection = None
