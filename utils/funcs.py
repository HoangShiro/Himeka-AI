import json, os, nltk, requests, discord, random, re
from nltk import word_tokenize, pos_tag
from translate import Translator
from langdetect import detect

from user_files.config import *

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

emojis = []

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

# Prompting
def extract_nouns(text):
    words = word_tokenize(text)
    text = process_nouns(words)
    tagged_words = pos_tag(text)
    ws = [word for word, tag in tagged_words if tag.startswith('JJ') or tag.startswith('VB') or tag.startswith('NN')]
    nn = " ".join(ws)
    return nn
def process_nouns(nouns):
    words_to_remove = [f"Himeka", "you", "me", "create", "image", "'m", "sorry",
                        "inaccuracy", "let", "do", "request", "please", "wait", "moment", 
                        "creating", "photo", "hmm", "make", "<3", "pic", "picture", "*", "rub", "draw"]
    replacement_dict = {
        "yourself": f"A cute Japanese girl with blonde hair in two pigtails, green eyes. Cute, bright, colorful colors."
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
    for word, replacement in re_text.items():
        final_text = text_emoji.replace(word, replacement)
    return final_text