# Discord integration

(The following information is accurate up to fd54cae48e0ae9c9b0d48c53094b0a312fbe12b1)

`example_bot.py` is an example of Discord integration. This sample connects to a bot set up by
Tirath, deployed on a sample server set up by Tirath, for demonstration purposes.

The bot listens for messages on the Discord server and downloads any attachments included in a
message.

![Discord message with two attachments downloaded by the bot](screenshot.png "Screenshot")

## Quickstart
* Follow base README.md quickstart instructions, then proceed.
* `BOT_TOKEN=$(cat ~/secrets/aipa.csrassist.test.txt) python example_bot.py`
