import asyncio
from characterai import PyAsyncCAI

from user_files.config import *


CAc = PyAsyncCAI(cai_key)
CAcr = c_token

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
