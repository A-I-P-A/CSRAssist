# Slack integration

The bot listens for messages on the Slack channels and downloads any attachments included in a
message, and then attempts to extract any text contained within the image.

![Slack message with 5 attachments downloaded by the bot](screenshot.png "Screenshot")

## Setup Slack App

https://www.kubiya.ai/resource-post/how-to-build-a-slackbot-with-python


## Quickstart
* Follow base README.md quickstart instructions, then proceed.
* `$ SLACK_BOT_TOKEN=<Slack Bot Token>`
* `$ SLACK_SIGNING_SECRET=<Slack Signing Secret>`
* `$ OPENAI_API_KEY=<OpenAI API Key>`
* `$ python slack_bot.py`
* Or a one-liner for the above commands: `SLACK_BOT_TOKEN=$(cat ~/secrets/aipa.csrassist.slack.test.SLACK_BOT_TOKEN.txt) SLACK_SIGNING_SECRET=$(cat ~/secrets/aipa.csrassist.slack.test.SLACK_SIGNING_SECRET.txt) OPENAI_API_KEY=$(cat ~/secrets/openai.txt) python slack_bot.py`
