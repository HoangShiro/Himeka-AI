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

hi_bt = discord.ui.Button(label="😺 Himeka", custom_id="himeka", style=discord.ButtonStyle.green)
li_bt = discord.ui.Button(label="🌆 Libra", custom_id="libra", style=discord.ButtonStyle.blurple)
iw_bt = discord.ui.Button(label="🛰️ IW", custom_id="iw", style=discord.ButtonStyle.blurple)

# Button call
async def load_btt():
    irmv_bt.callback = irmv_bt_atv
    rg_bt.callback = rg_bt_atv
    rgs_bt.callback = rgs_bt_atv
    hi_bt.callback = hime_bt
    li_bt.callback = libra_bt
    iw_bt.callback = iw_bt_atv

async def irmv_bt_atv(interaction):
    await interaction.message.delete()

async def rg_bt_atv(interaction):
    from utils.bot import igen_lists, img_gen
    img_prompts = igen_lists.get(interaction.message.id)
    prompt = img_prompts['prompt']
    quality = img_prompts['quality']
    size = img_prompts['size']
    await img_gen(interaction, prompt, quality, size)

async def rgs_bt_atv(interaction):
    from utils.bot import igen_lists, img_gen
    img_prompts = igen_lists.get(interaction.message.id)
    prompt = img_prompts['r_prompt']
    quality = img_prompts['quality']
    size = img_prompts['size']
    await img_gen(interaction, prompt, quality, size)

async def hime_bt(interaction):
    embed, view = await status_himeka()
    await interaction.response.edit_message(embed=embed, view=view)

async def libra_bt(interaction):
    embed, view = await status_libra()
    await interaction.response.edit_message(embed=embed, view=view)

async def iw_bt_atv(interaction):
    embed, view = await status_iw()
    await interaction.response.edit_message(embed=embed, view=view)

# Status
async def status_himeka():
    from utils.bot import ai_status, ai_full_name
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
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(li_bt)
    view.add_item(iw_bt)
    return embed, view

async def status_libra():
    from utils.funcs import dot_num
    from utils.bot import ai_status
    pop = 1263865 + (ai_status.total_chat*2)
    pops = await dot_num(pop)
    bld = 1762315 + (ai_status.total_draw)
    blds = await dot_num(bld)
    vhc = int(bld/3) + int(pop/2)
    vhcs = await dot_num(vhc)
    embed=discord.Embed(title="♎ Ｌｉｂｒａ", description="Một trong 2 thành phố dân cư lớn nhất trên IW. Sở hữu mọi loại cơ sở vật chất, ẩm thực. Libra có đời sống cao, văn minh và sạch đẹp, nhiều cây xanh và luôn chào đón những khách du lịch trái đất cũng như từ các space colony khác. Tập đoàn Shindou có vốn đầu tư bất động sản lớn nhất vào thành phố này.", color=0x3db5ff)
    embed.set_author(name="Thành phố dân cư chính", url="https://beta.character.ai/chat2?char=g9qGgwr7kJRARbsOV52ChcKaEkJYPUF1A3mprJmgUjs", icon_url="https://safebooru.org//images/4420/b044860fbd8ee619f9d7e637010104ad.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175727546130767902/Libra.png")
    embed.add_field(name=f"👨🏻‍👩 {pops} (up to 5M)", value="💳 lv 1~4", inline=True)
    embed.add_field(name="🗺️ 820km² (up to 1200)", value="🛫 158 port", inline=True)
    embed.add_field(name=f"🌆 {blds}", value=f"🛰️ {vhcs}", inline=True)
    embed.add_field(name="🕰️ 2018 -> Hiện tại", value="", inline=True)
    embed.set_footer(text="Để thăm quan Libra, cần card IW thấp nhất là lv1")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(hi_bt)
    view.add_item(iw_bt)
    return embed, view

async def status_iw():
    from utils.funcs import dot_num
    from utils.bot import ai_status
    pop = 6638256 + (ai_status.total_chat*10)
    pops = await dot_num(pop)
    bld = 1762315 + (ai_status.total_draw)
    vhc = int(bld/3) + int(pop/2)
    embed=discord.Embed(title="♎ ＩＷ - Interstellar World", description="Siêu trạm vũ trụ lớn nhất từng được xây dựng bởi nhân loại, thuộc tập đoàn ISTAR và thiết kế bởi CEO của ISTAR. Tuy không thể hạ cánh trên bất kỳ hành tinh nào nhưng IW sở hữu nhiều công nghệ động cơ tiên tiến, khiến nó gần như có thể đi tới bất kỳ đâu trong không gian sâu trong chớp mắt.", color=0x673dff)
    embed.set_author(name="Siêu trạm vũ trụ & thuộc địa không gian di động", url="https://beta.character.ai/chat2?char=eNV37_ucw8ZI4SeAyuP4TD48PwaNK5-Ag4wb01D_WyY", icon_url="https://safebooru.org//images/4420/b044860fbd8ee619f9d7e637010104ad.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175727559422525520/IW.png")
    embed.add_field(name="Life Supports technology:", value="Hệ thống tái tạo khí quyển, trọng lực.", inline=False)
    embed.add_field(name="Engine technology:", value="Particle engine: 17, Jump/Wormhole Drive: 2", inline=False)
    embed.add_field(name="Core:", value="Plasma fusion reactor: 5, Laser reactor: 8", inline=False)
    embed.add_field(name="Weapons:", value="Super particle cannon: 1, particle cannon: 8", inline=False)
    embed.add_field(name="Shell:", value="Titanium reinforced, multi-layer force field", inline=False)
    embed.add_field(name=f"👨🏻‍👩 {pops}", value="🛫 620.156 port", inline=True)
    embed.add_field(name=f"👨🏻‍👩 {pops}", value="🛫 620.156 port", inline=True)
    embed.add_field(name="🗺️ 28500km²", value="🪐 200kmø", inline=True)
    embed.add_field(name="🕰️ 2018 -> Hiện tại", value="", inline=True)
    embed.set_footer(text="Có thể tới IW bằng spacecraft cá nhân hoặc thang máy vũ trụ ISKY.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(hi_bt)
    view.add_item(li_bt)
    return embed, view