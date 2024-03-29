import asyncio
import json
import os
import re
import requests
import signal
import time
import pprint
from slack_bolt.async_app import AsyncApp
from typing import List

import sys
sys.path.insert(0, '..')
from ocr_integration import ocr
from stringlist_semantics import stringlist
from router import aipa

SERVER_PORT: int = 3000
ATTACHMENTS_DIR: str = "attachments"

token: str = os.getenv("SLACK_BOT_TOKEN")
app: AsyncApp = AsyncApp(
    token=token,
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

def split_words(user_message: str) -> List[str]:
    """Do this instead of split so that punctuation is also removed"""
    words = re.findall(r'\w+', user_message.lower())
    return words

slack_userid_to_name = {
    'U0676C3EQ4R': 'Tirath Ramdas',
}

task_state: str = "OPEN"  # TODO replace this with something more scalable, this is just a POC

@app.event("message")
async def event_message(event: dict, say) -> None:
    global task_state
    user_message: str = event.get('text')
    user_message_timestamp: int = int(float(event.get('ts')))

    attachments: List[dict] = []
    if event.get('files'):
        for file_info in event['files']:
            print('-----------NEW FILE----------------')
            pprint.pprint(file_info)
            file_name: str = file_info['name']
            download_path: str = os.path.join(ATTACHMENTS_DIR, file_name)
            response = requests.get(file_info['url_private_download'], headers={'Authorization': 'Bearer %s' % token})
            response.raise_for_status()
            with open(download_path, 'wb') as fd:
                fd.write(response.content)
            attachments.append({'path': download_path, 'name': file_name})

    # Sell My TV
    words_bag: List[str] = split_words(user_message)
    if task_state == 'SELL_MY_TV_AWAITING_PICS' or ('sell' in words_bag and 'tv' in words_bag):
        for attachment in attachments:
            text = ocr.extract_text([attachment['path']])
            attachment['stringlist'] = text
        pprint.pprint(attachments)
        if not attachments:
            await say('Ok, let\'s sell your TV! Please provide pics of your TV')
            task_state = 'SELL_MY_TV_AWAITING_PICS'
        else:
            ocr_snippets = []
            for attachment in attachments:
                ocr_snippets.extend(attachment['stringlist'])
            tv_description = stringlist.describe_tv(ocr_snippets)
            await say(f'Ok, let\'s sell your TV, {tv_description}')
            discord_payload = {}
            task_state = 'SELL_MY_TV_AWAITING_CSR'
            discord_payload['client'] = slack_userid_to_name[event['user']]
            discord_payload['task_state'] = task_state
            discord_payload['task_info'] = tv_description
            discord_payload['task_request_channel'] = 'Slack'
            discord_payload['user_message'] = user_message
            discord_payload['slack_timestamp'] = user_message_timestamp
            discord_payload['bot_timestmap'] = int(float(time.time()))
            pub_payload = json.dumps(discord_payload)
            aipa.publish_message(channel='discord', message=pub_payload)
    else:
        pprint.pprint(event)

if __name__ == "__main__":
    app.start(port = SERVER_PORT)
