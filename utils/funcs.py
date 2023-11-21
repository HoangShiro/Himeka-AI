import json, os, nltk, requests, discord, random, re, jaconv
import cv2, asyncio
import numpy as np

from discord import FFmpegPCMAudio
from nltk import word_tokenize, pos_tag
from translate import Translator
from mtranslate import translate
from langdetect import detect
from discord.ui import View

from utils.user_data import UserData
from utils.status import *
from utils.buttons import *
from utils.ai_api import *
from user_files.config import *

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

emojis = []
user_timers = {}

# Save json
def vals_save(file_name, variable_name, variable_value):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        data[variable_name] = variable_value
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file)
    except FileNotFoundError:
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file)
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Load json
def vals_load(file_name, variable_name):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        variable_value = data[variable_name]
        return variable_value
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None

# Prompting
def extract_nouns(text):
    words = word_tokenize(text)
    text = process_nouns(words)
    tagged_words = pos_tag(text)
    ws = [word for word, tag in tagged_words if tag.startswith('JJ') or tag.startswith('VB') or tag.startswith('NN')]
    nn = " ".join(ws)
    return nn
def process_nouns(nouns):
    words_to_remove = [f"himeka", "you", "me", "create", "image", "'m", "sorry",
                        "inaccuracy", "let", "do", "request", "please", "wait", "moment", 
                        "creating", "photo", "hmm", "make", "<3", "pic", "picture", "*", "rub", "draw",
                        "continue", "himeka", "generate", "art", "lem", "okay"]
    replacement_dict = {
        "yourself": f"A cute Japanese girl with blonde hair in two pigtails, green eyes. Cute, bright, colorful colors.",
        "iw": "a super giant ring-shaped space station connected to the center by shafts, in space, high technology architecture."
    }
    style = ", anime style"
    nouns = [replacement_dict.get(noun.lower(), noun) for noun in nouns if noun.lower() not in words_to_remove]
    nouns.append(style)
    return nouns

# Image save from url
async def dl_img(url, img_id):
    folder_path = "user_files/gen_imgs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = os.path.join(folder_path, f"{img_id}.png")

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Lỗi {response.status_code} khi tải ảnh từ URL.")

# Translate
def text_translate(text, target_lang):
    # Xác định ngôn ngữ của văn bản đầu vào
    source_lang = detect(text)
    
    # Kiểm tra xem ngôn ngữ đầu vào và ngôn ngữ đích có giống nhau hay không
    if source_lang == target_lang:
        return text
    
    # Dịch văn bản nếu ngôn ngữ đầu vào và ngôn ngữ đích khác nhau
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translated_text = translator.translate(text)
    return translated_text
def lang_detect(text):
    source_lang = detect(text)
    return source_lang

def text_translate2(text, to_language='ja'):
    translated_text = translate(text, to_language)
    return translated_text

# Romaji -> Katakana
def romaji_to_katakana(romaji_text):
    katakana_text = romaji_text.lower()
    katakana_text = jaconv.alphabet2kana(katakana_text)
    return katakana_text

# Text filter for tts
def remove_act(text):
    text = re.sub(r'\*([^*]+)\*', '', text)
    text = re.sub(r'\([^)]+\)', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'https?://\S+', '', text)
    return text

# Emoji load
def emojis_take(bot):
    global emojis
    guild = bot.get_guild(server_id)
    emojis = guild.emojis

# Text handle
def text_handle(text):
    # Emoji replace
    emoji_take = []
    emoji_name = None
    matches = re.finditer(r':([^:\s]+):', text)
    for match in matches:
        emoji_name = match.group(1).lower()
        for emoji in emojis:
            if re.search(rf'{emoji_name}', emoji.name.lower()):
                emoji_take.append(emoji)
    if emoji_take:
        chosen_emoji = random.choice(emoji_take)
    if emoji_name:
        text_emoji = text.replace(f':{emoji_name}:', str(chosen_emoji))
    else:
        text_emoji = text
    # Discord tag replace
    words = text_emoji.split()
    for i in range(len(words)):
        for key, value in re_text.items():
            match = re.search(key, words[i], re.IGNORECASE)
            if match:
                rtext = re_text[key]
                words[i] = words[i].replace(words[i], rtext)
    result = ' '.join(words)
    return result

# Reply message
async def mess_rep(message, mess, user_name, chat_log):
    from utils.bot import img_gen_chat, ai_status
    umess = "{}: {}".format(user_name, message.content)
    async with message.channel.typing():
        view = View(timeout=None)
        view.add_item(irmv_bt)
        answ, ain, busy = await CAI(umess)
        answ = text_handle(answ)
        if chat_log:
            print(umess)
            print(f"{ain}: {answ}")
            print()
        if busy:
            embed = await rena_notice(answ, user_name)
            if answ == "[sleep]":
                view.add_item(wu_bt)
            else:
                view.add_item(rcn_bt)
            await message.reply(embed=embed, view=view)
        else: 
            await message.reply(answ)
            asyncio.create_task(stt_inchat(user_name))
            uid = message.author.id
            u = UserData(uid)
            u.update('u_fame', 1)
        ai_status.update('total_chat', 1)
        asyncio.create_task(hime_tablet(message, answ, chat_log, user_name))
        await img_gen_chat(message, mess)

# Send message
async def mess_send(message, umess, chat_log):
    from utils.bot import ai_status
    async with message.channel.typing():
        answ, ain, busy = await CAI(umess)
        answ = text_handle(answ)
        if chat_log:
            print(umess)
            print(f"{ain}: {answ}")
            print()
        if not busy:
            await message.channel.send(answ)
            ai_status.update('total_chat', 1)
        await hime_tablet(message, answ, chat_log)

# Send message with channel id
async def mess_id_send(bot, ch_id, umess, chat_log):
    from utils.bot import ai_status
    channel = bot.get_channel(ch_id)
    async with channel.typing():
        answ, ain, busy = await CAI(umess)
        answ = text_handle(answ)
        if chat_log:
            print(umess)
            print(f"{ain}: {answ}")
            print()
        if not busy and answ != "[sleep]":
            await channel.send(answ)
            ai_status.update('total_chat', 1)
        async for message in channel.history(limit=1):
            pass
        await hime_tablet(message, answ, chat_log)
    return message

# Send voice
async def voice_send(url, ch):
    audio_source = FFmpegPCMAudio(url)
    await asyncio.sleep(0.5)
    ch.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)

# Voice make
async def voice_make_tts(mess, answ):
    from utils.bot import ai_status
    url = await tts_get(answ, speaker, pitch, intonation_scale, speed)
    if mess.guild.voice_client:
        b_ch = mess.guild.voice_client.channel.id
        b_vc = mess.guild.voice_client
        await voice_send(url, b_vc)
        ai_status.set('pr_vch_id', b_ch)

# Soundboard get
async def sob(sound_list, sound=None):
    audio_dir = "/sound"
    if not sound:
        audio_dir = f"./sound/{sound_list}"
        audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".wav")]
        audio_file = random.choice(audio_files)
    else:
        audio_file = f"{audio_dir}/{sound}"
    return audio_file

# Join voice channel
async def v_join(message):
    u_ch_id = message.author.voice.channel.id
    u_vc = message.author.voice.channel
    b_ch = None
    if message.guild.voice_client:
        b_ch = message.guild.voice_client.channel
        b_vc = message.guild.voice_client
    if b_ch and b_ch.id != u_ch_id:
        await b_vc.disconnect()
        await u_vc.connect()
    elif not b_ch:
        await u_vc.connect()

# Join voice channel
async def v_leave(message):
    from utils.bot import ai_status
    b_ch = None
    if message.guild.voice_client:
        b_ch = message.guild.voice_client.channel
        b_vc = message.guild.voice_client
    if b_ch:
        await b_vc.disconnect()
        pr_vch_id = None
        ai_status.set('pr_vch_id', pr_vch_id)

# Reconnect to voice channel
async def voice_rcn():
    from utils.bot import bot, ai_status
    pr_v = ai_status.pr_vch_id
    if pr_v:
        vc = await bot.get_channel(pr_v).connect()
        sound = await sob('greeting')
        await voice_send(sound, vc)

# Voice leave without chat
async def v_leave_nc():
    from utils.bot import bot, ai_status
    ch_id = ai_status.pr_vch_id
    if ch_id:
        vch = bot.get_channel(ch_id)
        vc = discord.utils.get(bot.voice_clients, guild=vch.guild)
        if vc and vc.is_connected():
            await vc.disconnect()

# Himeka's tablet
async def hime_tablet(mess, answ, chat_log, uname=None):
    from utils.bot import ai_name, ai_status
    # Voice
    if re.search(rf'vc|vo', answ, re.IGNORECASE) and re.search(rf'jo|ju', answ, re.IGNORECASE):
        if mess.author.voice and mess.author.voice.channel:
            await v_join(mess)
        else:
            if not ai_status.bot_ivd:
                umess = f"{ai_name}'s tablet: Can't find {uname} in any voice channel, ask {uname} for that."
                await mess_send(mess, umess, chat_log)
                ai_status.set('bot_ivd', True)
            pass
    if re.search(rf'vc|vo', answ, re.IGNORECASE) and re.search(rf'leav|out', answ, re.IGNORECASE):
        await v_leave(mess)
    
    # Status/IW's card
    if re.search(rf'my|hime|tôi|mình|tớ', answ, re.IGNORECASE) and re.search(rf'card|status|lv|thông|thẻ', answ, re.IGNORECASE) and re.search(rf'here|show|give|đây|ra|đưa', answ, re.IGNORECASE):
        embed, view = await status_himeka()
        await mess.channel.send(embed=embed, view=view)
    if re.search(rf'lev|lv', answ, re.IGNORECASE) and re.search(rf'of', answ, re.IGNORECASE) and re.search(rf'card', answ, re.IGNORECASE):
        embed, view = await status_card()
        await mess.channel.send(embed=embed, view=view)
    if re.search(rf'your|của bạn', answ, re.IGNORECASE) and re.search(rf'card|status|lv|thông|thẻ', answ, re.IGNORECASE) and re.search(rf'here|show|give|đây|ra|đưa|check|see', answ, re.IGNORECASE):
        embed, view = await status_user(mess)
        await mess.channel.send(embed=embed, view=view)

    # TTS
    if answ != "[sleep]":
        vc = None
        if mess.guild.voice_client:
            vc = mess.guild.voice_client.channel
        if mess.author.voice and mess.author.voice.channel:
            user_voice_channel = mess.author.voice.channel
            if vc and vc == user_voice_channel:
                await voice_make_tts(mess, answ)
     
# Count downt
async def count_down(user_timers, user):
    while user_timers[user] > 0:
        user_timers[user] -= 1
        await asyncio.sleep(1)
    del user_timers[user]

# Get IMG color
async def img_get_color(path):
    image = cv2.imread(path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([image_rgb], [0, 1, 2], None, [256, 256, 256], [100, 200, 100, 200, 100, 200])
    max_index = np.unravel_index(hist.argmax(), hist.shape)
    r, g, b = int(max_index[0]), int(max_index[1]), int(max_index[2])

    cmin = 30
    cmax = 240
    if r < cmin:
        r += cmin
    if g < cmin:
        g += cmin
    if b < cmin:
        b += cmin
    if r > cmax:
        r -= cmin
    if g > cmax:
        g -= cmin
    if b > cmax:
        b -= cmin

    return r, g, b

# Add dot to number
async def dot_num(number):
        num_str = str(number)
        num_digits = len(num_str)
        formatted_str = ""
        for i in range(num_digits - 1, -1, -1):
            formatted_str = num_str[i] + formatted_str
            if (num_digits - i) % 3 == 0 and i != 0:
                formatted_str = "." + formatted_str 
        return formatted_str

# Check cai chat
async def check_cai_ready(answ):
    from utils.bot import bot, ai_status
    ready = True
    if "error" in answ:
        if ai_status.bot_cls < 1:
            ai_status.update('bot_cls', 1)
            await bot.close()
        else:
            ready = False
        return ready
    else:
        if ai_status.bot_cls != 0:
            ai_status.set('bot_cls', 0)
        return ready

async def money_with_hime():
    from utils.bot import ai_status
    uids = ai_status.u_in_vc
    if uids:
        for uid in uids:
            u = UserData(uid)
            u.update('u_blc', 5)