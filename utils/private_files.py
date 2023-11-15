# Tự động tạo ra các file cho user nếu thiếu
import os
import json

# openai key list
openai_key = {
    "oak_1": '',
    "oak_2": '',
    "oak_3": '',
    "oak_4": '',
    "oak_5": '',
}

# Config.py
vals_list = {
    "cai_key": '',
    "c_token": '',
    "discord_bot_key": '',
    "vv_key": '',
    "ower_id": 0,
    "server_id": 0,
    "speaker": 47,
    "voice_low": 49,
    "voice_high": 48,
    "voice_asmr": 50,
    "pitch": 0,
    "intonation_scale": 1.5,
    "speed": 1
}

# Emo list
mood_names = {
    "angry": "sulking",
    "sad": "sad",
    "lonely": "a bit lonely",
    "normal": "chilling",
    "happy": "happily",
    "excited": "so happy",
    "like": "feeling loved",
    "love": "so loved",
    "obsess": "Obsessive love",
    "yandere": "Yandere ♥️"
}

# vals.json
default_values = {
    "bot_mood": 0
}

def json_update(path, vals):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            json.load(file)
    except FileNotFoundError:
        with open(path, 'w', encoding="utf-8") as file:
            json.dump(vals, file)

def update_cfg(path, vals):
    if not os.path.exists(path):
        # Nếu tệp config.py không tồn tại, tạo nó và thêm các biến
        with open(path, "w", encoding="utf-8") as config_file:
            for key, value in vals.items():
                config_file.write(f"{key} = {repr(value)}\n")
    else:
        # Nếu tệp config.py đã tồn tại, kiểm tra và thêm các biến nếu chưa tồn tại
        with open(path, "r", encoding="utf-8") as config_file:
            existing_content = config_file.read()
            for key, value in vals.items():
                if key not in existing_content:
                    # Nếu biến không tồn tại, thêm nó vào tệp
                    with open(path, "a") as config_file:
                        config_file.write(f"{key} = {repr(value)}\n")

if __name__ == '__main__':
    update_cfg("user_files/config.py", vals_list)
    update_cfg("user_files/openai_key.py", openai_key)
    update_cfg("user_files/moods.py", mood_names)
    json_update('user_files/vals.json', default_values)