import asyncio
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

task_state: str = "OPEN"  # TODO replace this with something more scalable, this is just a POC

@app.event("message")
async def event_message(event: dict, say) -> None:
    async def event_message(event: dict, say) -> None:
        global task_state
        user_message: str = event.get('text')
        attachments: List[dict] = []
        if event.get('files'):
            for file_info in event['files']:
                print('---------------------------')
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
                task_state = 'SELL_MY_TV_AWAITING_CSR'
        else:
            pprint.pprint(event)

if __name__ == "__main__":
    app.start(port = int(os.getenv("SERVER_PORT", SERVER_PORT)))
