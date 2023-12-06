import queue
import redis
import threading
import time


redis_client: redis.StrictRedis = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
listen_queues = {}


def listen_to_channel(channel: str) -> None:
    """
    Must call initialize_channel before calling this.
    """
    global listen_queues
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)

    while not listen_queues[channel]['stop']:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            listen_queues[channel]['queue'].put(message['data'])
        time.sleep(1)


def initialize_channel_listener(channel: str) -> None:
    global listen_queues
    listen_queues[channel] = {}
    listen_queues[channel]['queue'] = queue.Queue()
    listen_queues[channel]['stop'] = False
    listen_queues[channel]['thread'] = threading.Thread(target=listen_to_channel, args=(channel,))
    listen_queues[channel]['thread'].start()


def stop_channel_listener(channel: str) -> None:
    global listen_queues
    listen_queues[channel]['stop'] = True
    listen_queues[channel]['thread'].join()
    del listen_queues[channel]
    print(f'Stopped listener for {channel}')


def get_message_from_channel(channel: str) -> str:
    global listen_queues
    if listen_queues[channel]['queue'].empty():
        return None
    else:
        return listen_queues[channel]['queue'].get()


def publish_message(channel: str, message: str) -> None:
    print(f'Publishing {message} to {channel}')
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


def test():
    """
    In another console, do the following:
    >>> import redis
    >>> redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    >>> redis_client.publish('test', 'foo')
    >>> redis_client.publish('test', 'bar')
    """
    initialize_channel_listener('test')
    count = 0
    while count < 3:
        print('Let\'s poll...')
        msg = get_message_from_channel('test')
        if msg:
            print(f"Received message: {msg}")
            count += 1
        else:
            time.sleep(1)
    stop_channel_listener('test')

if __name__ == '__main__':
    test()

