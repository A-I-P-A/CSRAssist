import asyncio
import os
import requests
import signal
import time
import pprint
from slack_bolt.async_app import AsyncApp

import sys
sys.path.insert(0, '..')
from ocr_integration import ocr

SERVER_PORT = 3000
ATTACHMENTS_DIR = "attachments"

token = os.getenv("SLACK_BOT_TOKEN")
app = AsyncApp(
    token = token,
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")
)

@app.event("message")
async def event_message(event, say):
    if event.get('files') is None:
        await say('Please upload some images')
        return
    
    print(f'Message received. client_msg_id: {event["client_msg_id"]}, channel: {event["channel"]}, user: {event["user"]}, type: {event["type"]}, subtype: {event["subtype"]}, text: {event["text"]}, files: {len(event["files"])}')
    for file in event['files']:
        file_name = file['name']
        download_path = os.path.join(ATTACHMENTS_DIR, file_name)
        response = requests.get(file['url_private_download'], headers={'Authorization': 'Bearer %s' % token})
        response.raise_for_status
        with open(download_path, 'wb') as file:
            file.write(response.content)
        await say(f'Downloaded file {file_name}')
        text = ocr.extract_text([download_path])
        await say(f'OCR text: {text}')
    await say(f'ACK message of len {len(event)}')
    print(f'Message processing completed. client_msg_id: {event["client_msg_id"]}')

if __name__ == "__main__":
    app.start(port = int(os.getenv("SERVER_PORT", SERVER_PORT)))

