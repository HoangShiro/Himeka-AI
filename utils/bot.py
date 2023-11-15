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

@bot.event
async def on_ready():
    print("Himeka đã khởi động")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    user_name = message.author.nick
    if not user_name:
        user_name = message.author.name
    result = "{}: {}".format(user_name, message.content)
    print(result)
    # Phản hồi chat
    async with message.channel.typing():
        answ, ain = await CAI(result)
        print(f"{ain}: {answ}")
        print()
        await message.reply(answ)

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

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    bot_run()