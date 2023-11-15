import asyncio
from characterai import PyAsyncCAI
import discord
from discord.ext import commands, tasks
from discord.ui import View, button

from user_files.config import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

CAc = PyAsyncCAI(cai_key)
CAcr = c_token

ai_name = "Himeka"
ai_last = "Shindou"
ai_full_name = f"{ai_name} {ai_last}"

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
        print(umess)
        async with message.channel.typing():
            answ, ain = await CAI(umess)
            print(f"{ain}: {answ}")
            print()
            await message.reply(answ)
    
    return

# Hàm Chat
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

# Các câu lệnh
@bot.tree.command(name="renew", description=f"Khởi động lại {ai_name}.")
async def renew(interaction: discord.Interaction):
    await interaction.response.send_message(f"{ai_name} sẽ sớm quay lại nè~!", ephemeral=True)
    await bot.close()

@bot.tree.command(name="newchat", description="Cuộc trò chuyện mới.")
async def newchat(interaction: discord.Interaction):
    await interaction.response.send_message(f"*Quay ngược thời gian lúc {ai_name} mới tham gia NekoArt Studio... 🕒*")
    CAc.chat.new_chat(c_token)

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    bot_run()