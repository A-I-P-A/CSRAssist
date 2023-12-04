import redis
import threading

redis_client: redis.StrictRedis = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def publish_message(channel: str, message: str) -> None:
    redis_client.publish(channel, message)

def check_for_messages_blocking(channel: str) -> str:
    """
    This function blocks until a message is received on the specified channel.
    """
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            return message['data']

def check_for_messages_nonblocking(channel: str) -> str:
    return timeout_wrapper(check_for_messages_blocking, timeout=2, channel=channel)

def timeout_wrapper(func, timeout=1, *args, **kwargs):
    """
    Wraps a blocking function to add a timeout.

    Args:
    func (callable): The function to wrap.
    timeout (int, optional): Timeout duration in seconds. Defaults to 1.
    *args: Variable length argument list for the function.
    **kwargs: Arbitrary keyword arguments for the function.

    Returns:
    The result of the function if it completes in time, or None otherwise.
    """
    result_container = []

    def wrapper(*args, **kwargs):
        result_container.append(func(*args, **kwargs))

    thread = threading.Thread(target=wrapper, args=args, kwargs=kwargs)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None
    else:
        return result_container[0] if result_container else None


if __name__ == '__main__':
    """
    In another console, do the following:
    >>> import redis
    >>> redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    >>> redis_client.publish('test', 'foo')
    >>> redis_client.publish('test', 'bar')
    """
    while True:
        print('Let\'s poll...')
        print(timeout_wrapper(check_for_messages_blocking, timeout=5, channel='test'))

