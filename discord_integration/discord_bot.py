import asyncio
import discord
from discord.ext import tasks
import json
import os
import requests
import signal

import sys
sys.path.insert(0, '..')
from router import aipa

import pprint

CHANNEL_ID = 1176399154210160652
ATTACHMENTS_DIR = "attachments"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def signal_handler(sig, frame):
    print("Received signal:", sig)
    long_poll.stop()
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(shutdown_bot())
    else:
        loop.run_until_complete(shutdown_bot())
    aipa.stop_channel_listener('discord')

async def shutdown_bot():
    print("Bot is shutting down...")
    # Perform any cleanup here
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('CSRAssist going offline 😴')
    await client.close()

@tasks.loop(seconds=10)
async def long_poll():
    channel = client.get_channel(CHANNEL_ID)
    draining = True
    while draining:
        msgs = aipa.get_message_from_channel('discord')
        if msgs:
            pprint.pprint(msgs)
            await channel.send(msgs)
        else:
            draining = False

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('CSRAssist online 👋🏽')
    aipa.initialize_channel_listener('discord')
    long_poll.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print(message.content)

        await message.channel.send(f'ACK message of len {len(message.content)}')
        pprint.pprint(message)

def register_termination_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise Exception("DISCORD_BOT_TOKEN not defined")
    register_termination_handlers()
    client.run(token)
