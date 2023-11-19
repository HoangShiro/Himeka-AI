import discord
from discord.ui import View

rmv_bt = discord.ui.Button(label="➖", custom_id="remove", style=discord.ButtonStyle.grey)
irmv_bt = discord.ui.Button(label="➖", custom_id="remove", style=discord.ButtonStyle.grey)
rc_bt = discord.ui.Button(label="💫 re chat", custom_id="rc", style=discord.ButtonStyle.grey)
rg_bt = discord.ui.Button(label="💫", custom_id="rg", style=discord.ButtonStyle.blurple)
continue_bt = discord.ui.Button(label="✨ continue", custom_id="continue", style=discord.ButtonStyle.grey)
rgs_bt = discord.ui.Button(label="✨ similar", custom_id="rgs", style=discord.ButtonStyle.green)
nt_bt = discord.ui.Button(label="🔆 next", custom_id="next", style=discord.ButtonStyle.green)
bk_bt = discord.ui.Button(label="🔅 back", custom_id="back", style=discord.ButtonStyle.green)

st_bt1 = discord.ui.Button(label="❤️", custom_id="st1", style=discord.ButtonStyle.grey)
st_bt2 = discord.ui.Button(label="❤️", custom_id="st2", style=discord.ButtonStyle.grey)
st_bt3 = discord.ui.Button(label="❤️", custom_id="st3", style=discord.ButtonStyle.grey)

# Status
async def status_make():
    from utils.bot import ai_status
    async def set_emood(bot_mood):
        bot_mood = max(1, min(bot_mood, 99))
        emood_count = (bot_mood+20) // 20
        emood = "✨" * emood_count
        return emood
    
    emood = await set_emood(ai_status.bot_mood)
    embed=discord.Embed(title=f"{ai_full_name}", description="IW's card lv: 4", color=0xffa3af)
    embed.set_author(name="The Head of Libra's city", url="https://beta.character.ai/chat2?char=g9qGgwr7kJRARbsOV52ChcKaEkJYPUF1A3mprJmgUjs",
                     icon_url="https://safebooru.org//images/4420/b044860fbd8ee619f9d7e637010104ad.png")
    embed.set_thumbnail(url="https://safebooru.org//images/4420/b044860fbd8ee619f9d7e637010104ad.png")
    embed.add_field(name="Status", value="Happily in NekoArt Studio", inline=False)
    embed.add_field(name="Mood", value=emood, inline=True)
    embed.add_field(name="Likeable", value="💖💖💖", inline=True)
    embed.add_field(name="💬 Chats", value=ai_status.total_chat, inline=True)
    embed.add_field(name="🎨 Drew", value=ai_status.total_draw, inline=True)
    embed.add_field(name="🔄️ Connected", value=ai_status.total_rcn, inline=True)
    embed.add_field(name="🕒 Time leap", value=ai_status.roll_back, inline=True)
    view = View()
    view.add_item(irmv_bt)
    return embed, view