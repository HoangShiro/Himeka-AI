import asyncio
import discord
from discord.ext import commands, tasks
from discord.ui import View, button
import json, os

from user_files.config import *
from utils.ai_api import *
from utils.funcs import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ai_name = "Himeka"
ai_last = "Shindou"
ai_full_name = f"{ai_name} {ai_last}"

# Vals.json
bot_mood = 50
chat_log = False
cds_log = True
st_log = False

default_values = {
    "bot_mood": 50.0,
    "chat_log": False,
    "cds_log": True,
    "st_log": False
}

# Kiểm tra xem tệp JSON có tồn tại không
try:
    with open('user_files/vals.json', 'r', encoding="utf-8") as file:
        data3 = json.load(file)
except FileNotFoundError:
    with open('user_files/vals.json', 'w', encoding="utf-8") as file:
        json.dump(default_values, file)
    # Nếu tệp không tồn tại, sử dụng giá trị mặc định
    data3 = default_values

# Gán giá trị từ data cho các biến hiện tại
for key, value in default_values.items():
    globals()[key] = data3.get(key, value)

    # Dừng sau khi đã duyệt qua tất cả các phần tử trong default_values
    if key == list(default_values.keys())[-1]:
        break

# Kiểm tra và thêm biến thiếu vào tệp JSON nếu cần
for key, value in default_values.items():
    if key not in data3:
        data3[key] = value

# Cập nhật tệp JSON với các biến mới nếu có
with open('user_files/vals.json', 'w', encoding="utf-8") as file:
    json.dump(data3, file)

@bot.event
async def on_ready():
    # Đồng bộ hoá commands
    try:
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ {len(synced)} lệnh.")
    except Exception as e:
        print(e)
    print("Himeka đã khởi động")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Phản hồi chat
    if message.content:
        user_name = message.author.nick
        if not user_name:
            user_name = message.author.name
        umess = "{}: {}".format(user_name, message.content)
        
        async with message.channel.typing():
            answ, ain = await CAI(umess)
            if chat_log:
                print(umess)
                print(f"{ain}: {answ}")
                print()
            await message.reply(answ)
    
    return

# Các câu lệnh
@bot.tree.command(name="renew", description=f"Khởi động lại {ai_name}.")
async def renew(interaction: discord.Interaction):
    await interaction.response.send_message(f"{ai_name} sẽ sớm quay lại nè~!", ephemeral=True)
    await bot.close()

@bot.tree.command(name="newchat", description="Cuộc trò chuyện mới.")
async def newchat(interaction: discord.Interaction):
    iuser = interaction.user.name
    await interaction.response.send_message(f"*Đã quay ngược thời gian lúc {ai_name} mới tham gia NekoArt Studio... 🕒*")
    await CAc.chat.new_chat(c_token)
    if cds_log:
        print(f"[NEW CHAT] - {iuser}")
        print()

@bot.tree.command(name="clogs", description=f"Toggle console log.")
async def cslog(interaction: discord.Interaction, chat: bool = False, command: bool = True, status: bool = False):
    global chat_log, cds_log, st_log
    if interaction.user.id == dev_id:
        chat_log = chat
        cds_log = command
        st_log = status
        await interaction.response.send_message(f"`Chat log: {chat_log}, Command log: {cds_log}, Status log: {st_log}.`", ephemeral=True)
        vals_save('user_files/vals.json', 'chat_log', chat_log)
        vals_save('user_files/vals.json', 'cds_log', cds_log)
        vals_save('user_files/vals.json', 'st_log', st_log)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name}'s DEV mới có thể sử dụng lệnh này.`", ephemeral=True)

@bot.tree.command(name="ping", description=f"Test commands")
async def test_cmd(interaction: discord.Interaction):
    if interaction.user.id == dev_id:
        ntc = test_key()
        print(ntc)
        await interaction.response.send_message(f"Pong~!", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name}'s DEV mới có thể sử dụng lệnh này.`", ephemeral=True)

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    bot_run()