# AIPA Router

(The following information is accurate up to 032cd495af775114194fb91f9cfc54cc968f9fbf)

A pubsub service may serve as a 'router' to integrate the various agents and tools AIPA
may utilise to deliver quality service.

We are using redis as a pub/sub service. This requires installing Redis; on Ubuntu 20 do
`sudo apt install redis`.

If when running slack_integration or discord_integration you encounter an exception that
looks like this:
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```
It is probably because you didn't install Redis.

If you experience any issues like missing messages, the following may help with debugging:
```
redis-cli
MONITOR
```