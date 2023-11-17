import json, os, nltk, requests, discord, random, re, jaconv
from discord import FFmpegPCMAudio
from nltk import word_tokenize, pos_tag
from translate import Translator
from langdetect import detect

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
        "iw": "a giant ring-shaped space station connected to the center by shafts, in space, high technology architecture."
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
        text_emoji = text_emoji.lower()
    else:
        text_emoji = text.lower()
    # Discord tag replace
    words = text_emoji.split()
    for i in range(len(words)):
        for key, value in re_text.items():
            match = re.search(key, words[i], re.IGNORECASE)
            if match:
                rtext = re_text[key]
                words[i] = words[i].replace(words[i], rtext)
    result = ' '.join(words)
    num = result.count("!")
    if num > 1:
        result = "### " + result
    elif num > 2:
        result = "## " + result
    elif num > 3:
        result = "# " + result
    return result

# Reply message
async def mess_rep(message, mess, umess, chat_log):
    from utils.bot import img_gen_chat
    async with message.channel.typing():
        answ, ain = await CAI(umess)
        answ = text_handle(answ)
        if chat_log:
            print(umess)
            print(f"{ain}: {answ}")
            print()
        await message.reply(answ)
        asyncio.create_task(hime_tablet(message, answ))
        await img_gen_chat(message, mess)
# Send message
async def mess_send(message, umess, chat_log):
    async with message.channel.typing():
        answ, ain = await CAI(umess)
        answ = text_handle(answ)
        if chat_log:
            print(umess)
            print(f"{ain}: {answ}")
            print()
        await message.channel.send(answ)
        await hime_tablet(message, answ)

# Send message with channel id
async def mess_id_send(bot, ch_id, umess, chat_log):
    channel = bot.get_channel(ch_id)
    async with channel.typing():
        answ, ain = await CAI(umess)
        answ = text_handle(answ)
        if chat_log:
            print(umess)
            print(f"{ain}: {answ}")
            print()
        await channel.send(answ)
        async for message in channel.history(limit=1):
            pass
        await hime_tablet(message, answ)
    return message

# Send voice
async def voice_send(url, ch):
    audio_source = FFmpegPCMAudio(url)
    await asyncio.sleep(0.5)
    ch.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)

# Voice make
async def voice_make_tts(mess, answ):
    url = await tts_get(answ, speaker, pitch, intonation_scale, speed)
    if mess.guild.voice_client:
        b_ch = mess.guild.voice_client.channel.id
        b_vc = mess.guild.voice_client
        await voice_send(url, b_vc)
        vals_save('user_files/vals.json', 'pr_vch_id', b_ch)

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
    b_ch = None
    if message.guild.voice_client:
        b_ch = message.guild.voice_client.channel
        b_vc = message.guild.voice_client
    if b_ch:
        await b_vc.disconnect()
        pr_vch_id = None
        vals_save('user_files/vals.json', 'pr_vch_id', pr_vch_id)

# Himeka's tablet
async def hime_tablet(mess, answ):
    # Voice
    if re.search(rf'vc', answ, re.IGNORECASE) and re.search(rf'join', answ, re.IGNORECASE):
        if mess.author.voice and mess.author.voice.channel:
            await v_join(mess)
    if re.search(rf'vc', answ, re.IGNORECASE) and re.search(rf'leav', answ, re.IGNORECASE):
        await v_leave(mess)

    # TTS
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