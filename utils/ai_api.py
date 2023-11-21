import asyncio, requests
from characterai import PyAsyncCAI
from openai import AsyncOpenAI

from utils.prompting import *
from user_files.openai_key import *
from user_files.config import *

alt_trans = False

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
    from utils.bot import ai_name, ai_status
    CAc = PyAsyncCAI(cai_key)
    CAcr = c_token
    name = "Rena"
    busy = True
    if not ai_status.sleeping:
        try:
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

            busy = False
            await ai_status.set('ai_busy', False)
            await asyncio.sleep(15)
            print("TEST OK")
        except Exception as e:
            text = "error"
            await ai_status.set('ai_busy', True)
            print("CAI error: ", str(e))
    else:
        text = "[sleep]"
    return text, name, busy

# Tasks - Openai
async def openai_task(case):
    key = oa_key.get_key()
    client = AsyncOpenAI(api_key=key, timeout=60)
    prompt = getPrompt_task(case)

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=1024,
        temperature=1,
        top_p=0.9
    )
    task = response.choices[0].message.content
    return task

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

# TTS - VoiceVox
async def tts_get(text, speaker, pitch, intonation_scale, speed):
    from utils.funcs import remove_act, romaji_to_katakana, text_translate, text_translate2, vals_load
    global alt_trans
    translated = None
    if not alt_trans:
        translated = text_translate(text, "ja")
        if "MYMEMORY WARNING:" in translated:
            translated = text_translate2(text, "ja")
            alt_trans = True
    else:
        translated = text_translate2(text, "ja")
    text_fill = remove_act(translated)
    if not text_fill:
        if not text:
            text = "エラー エラー"
        text_fill = text
    cnv_text = romaji_to_katakana(text_fill)
    url = f"https://deprecatedapis.tts.quest/v2/voicevox/audio/?key={vv_key}&text={cnv_text}&speaker={speaker}&pitch={pitch}&intonationScale={intonation_scale}&speed={speed}"
    
    """response = requests.get(url)
    st_log = await vals_load('user_files/vals.json', 'st_log')

    if response.status_code == 200:
        with open('user_files/ai_voice_msg.ogg', 'wb') as f:
            f.write(response.content)
        if st_log:
            print(f"Voice đã được tải về thành công.")
    else:
        print(f"Lỗi khi tạo voice, mã lỗi: {response.status_code}")"""
    
    return url