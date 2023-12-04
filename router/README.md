We are using redis as a pub/sub service. This requires installing Redis; on Ubuntu 20 do
`sudo apt install redis`.

If when running slack_integration or discord_integration you encounter an exception that
looks like this:
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```
It is probably because you didn't install Redis.