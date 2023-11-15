import asyncio
from characterai import PyAsyncCAI
from openai import AsyncOpenAI
from user_files.openai_key import *

from user_files.config import *
from user_files.openai_key import *

CAc = PyAsyncCAI(cai_key)
CAcr = c_token

# Roll key
class KeyM:
    def __init__(self):
        self.values = [value for name, value in globals().items() if name.startswith("oak_")]
        self.cid = 0

    def get_key(self):
        ckey = self.values[self.cid]
        self.cid = (self.cid + 1) % len(self.values)
        return ckey
    
oa_key = KeyM()

# Chat - CAI
async def CAI(message):
    chat = await CAc.chat.get_chat(CAcr)
    participants = chat['participants']

    # In the list of "participants",
    # a character can be at zero or in the first place
    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    data = await CAc.chat.send_message(
        chat['external_id'], tgt, message
    )

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']
    
    return text, name

# Image generate - Openai
async def openai_images(prompt, quality, size):
    key = oa_key.get_key()
    client = AsyncOpenAI(api_key=key, timeout=60)
    response = await client.images.generate(
        prompt=prompt,
        model="dall-e-3",
        quality=quality,
        response_format="url",
        size=size
    )
    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt
    return image_url, revised_prompt

def test():
    key = oa_key.get_key()
    return key