import asyncio
import discord
import os
import requests
import signal

import sys
sys.path.insert(0, '..')
from ocr_integration import ocr

import pprint

CHANNEL_ID = 1176399154210160652
ATTACHMENTS_DIR = "attachments"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def signal_handler(sig, frame):
    print("Received signal:", sig)
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(shutdown_bot())
    else:
        loop.run_until_complete(shutdown_bot())

async def shutdown_bot():
    print("Bot is shutting down...")
    # Perform any cleanup here
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('CSRAssist going offline 😴')
    await client.close()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('CSRAssist online 👋🏽')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print(message.content)
        for attachment in message.attachments:
            response = requests.get(attachment.url)
            download_path = os.path.join(ATTACHMENTS_DIR, attachment.filename)
            with open(download_path, 'wb') as file:
                file.write(response.content)
            await message.channel.send(f'Downloaded file {attachment.filename}')
            text = ocr.extract_text([download_path])
            await message.channel.send(f'OCR text: {text}')

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