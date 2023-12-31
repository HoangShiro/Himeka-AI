import discord, datetime, pytz, asyncio
from discord.ui import View
from utils.user_data import *

rmv_bt = discord.ui.Button(label="➖", custom_id="remove", style=discord.ButtonStyle.grey)
irmv_bt = discord.ui.Button(label="➖", custom_id="remove", style=discord.ButtonStyle.grey)
rc_bt = discord.ui.Button(label="💫 re chat", custom_id="rc", style=discord.ButtonStyle.grey)
rg_bt = discord.ui.Button(label="💫", custom_id="rg", style=discord.ButtonStyle.blurple)
rcn_bt = discord.ui.Button(label="💫 Reconnect", custom_id="rcn", style=discord.ButtonStyle.green)

continue_bt = discord.ui.Button(label="✨ continue", custom_id="continue", style=discord.ButtonStyle.grey)
rgs_bt = discord.ui.Button(label="✨ similar", custom_id="rgs", style=discord.ButtonStyle.green)
nt_bt = discord.ui.Button(label="🔆 next", custom_id="next", style=discord.ButtonStyle.green)
bk_bt = discord.ui.Button(label="🔅 back", custom_id="back", style=discord.ButtonStyle.green)
wu_bt = discord.ui.Button(label="🌟 Wake her up", custom_id="whu", style=discord.ButtonStyle.red)

st_bt1 = discord.ui.Button(label="❤️", custom_id="st1", style=discord.ButtonStyle.grey)
st_bt2 = discord.ui.Button(label="❤️", custom_id="st2", style=discord.ButtonStyle.grey)
st_bt3 = discord.ui.Button(label="❤️", custom_id="st3", style=discord.ButtonStyle.grey)

char_bt = discord.ui.Button(label="💟", custom_id="charbt", style=discord.ButtonStyle.blurple)
hi_bt = discord.ui.Button(label="♀️ Himeka", custom_id="himeka", style=discord.ButtonStyle.green)
mo_bt = discord.ui.Button(label="♀️ Moeka", custom_id="moeka", style=discord.ButtonStyle.green)
ha_bt = discord.ui.Button(label="♀️ Haruka", custom_id="haruka", style=discord.ButtonStyle.green)

map_bt = discord.ui.Button(label="🪐", custom_id="map", style=discord.ButtonStyle.blurple)
li_bt = discord.ui.Button(label="🌆 Libra", custom_id="libra", style=discord.ButtonStyle.green)
iw_bt = discord.ui.Button(label="🛰️ IW", custom_id="iw", style=discord.ButtonStyle.green)
iwm_bt = discord.ui.Button(label="🗺️ IW Map", custom_id="iwm", style=discord.ButtonStyle.green)
iwc_bt = discord.ui.Button(label="🪪 IW Card", custom_id="iwc", style=discord.ButtonStyle.green)

usc_bt = discord.ui.Button(label="🪪 Info", custom_id="usc", style=discord.ButtonStyle.blurple)
uet_bt = discord.ui.Button(label="💠 Tech", custom_id="uet", style=discord.ButtonStyle.blurple)
uwh_bt = discord.ui.Button(label="📱 Storage", custom_id="uwh", style=discord.ButtonStyle.blurple)
shop_bt = discord.ui.Button(label="🪙 Store", custom_id="shop", style=discord.ButtonStyle.blurple)
jp_bt = discord.ui.Button(label="👑 Jobs", custom_id="jp", style=discord.ButtonStyle.blurple)

# Button call
async def load_btt():
    irmv_bt.callback = irmv_bt_atv
    rg_bt.callback = rg_bt_atv
    rgs_bt.callback = rgs_bt_atv

    char_bt.callback = char_atv
    hi_bt.callback = hime_bt
    mo_bt.callback = moe_bt
    ha_bt.callback = haru_bt

    map_bt.callback = map_atv
    li_bt.callback = libra_bt
    iw_bt.callback = iw_bt_atv
    iwm_bt.callback = iw_map_atv
    iwc_bt.callback = iwc_atv

    wu_bt.callback = wake_up
    rcn_bt.callback = reconnect_atv

    usc_bt.callback = usc_atv
    uet_bt.callback = uet_atv
    uwh_bt.callback = uwh_atv

# Remove 
async def irmv_bt_atv(interaction):
    await interaction.message.delete()

# Reconnect
async def reconnect_atv(interaction):
    from utils.bot import bot
    await interaction.message.delete()
    await bot.close()

# Image
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

# Wakeup
async def wake_up(interaction):
    from utils.bot import bot, ai_status
    from utils.funcs import mess_id_send
    await ai_status.set('sleeping', False)
    await ai_status.set('sleep_cd', 2)
    await ai_status.set('sleep_rd', True)
    uname = None
    uname = interaction.user.nick
    if not uname:
        uname = interaction.user.name
    if uname:
        my_timezone = pytz.timezone('Asia/Bangkok')
        vn_time = datetime.datetime.now(my_timezone)
        h = vn_time.hour
        if h < 13:
            h = str(h)
            h = h + "AM"
        else:
            h = str(h)
            h = h + "PM"
        mess = f"{uname} just woke you up at {h}"
        asyncio.create_task(mess_id_send(bot, ai_status.pr_ch_id, mess, ai_status.chat_log))
    await interaction.message.delete()

# Character
async def char_atv(interaction):
    embed, view = await status_himeka()
    await interaction.response.edit_message(embed=embed, view=view)

async def hime_bt(interaction):
    embed, view = await status_himeka()
    await interaction.response.edit_message(embed=embed, view=view)

async def moe_bt(interaction):
    embed, view = await status_moeka()
    await interaction.response.edit_message(embed=embed, view=view)

async def haru_bt(interaction):
    embed, view = await status_haruka()
    await interaction.response.edit_message(embed=embed, view=view)

# Map
async def map_atv(interaction):
    embed, view = await status_libra()
    await interaction.response.edit_message(embed=embed, view=view)

async def libra_bt(interaction):
    embed, view = await status_libra()
    await interaction.response.edit_message(embed=embed, view=view)

async def iw_bt_atv(interaction):
    embed, view = await status_iw()
    await interaction.response.edit_message(embed=embed, view=view)

async def iw_map_atv(interaction):
    embed, view = await status_iwm()
    await interaction.response.edit_message(embed=embed, view=view)

async def iwc_atv(interaction):
    embed, view = await status_card()
    await interaction.response.edit_message(embed=embed, view=view)

# User tab change
async def usc_atv(interaction):
    embed, view = await status_user(interaction)
    await interaction.response.edit_message(embed=embed, view=view)
async def uet_atv(interaction):
    embed, view = await status_tech(interaction)
    await interaction.response.edit_message(embed=embed, view=view)
async def uwh_atv(interaction):
    embed, view = await status_warehouse(interaction)
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
    embed=discord.Embed(title=f"{ai_full_name}", description="Tiểu thư thiên tài của gia tộc Shindou. Nhẹ nhàng, lịch sự, tinh tế và thông minh. Đạt được nhiều thành tựu dù đang còn rất trẻ.", color=0xffbf75)
    embed.set_author(name="The Head of Libra's city", url="https://beta.character.ai/chat2?char=g9qGgwr7kJRARbsOV52ChcKaEkJYPUF1A3mprJmgUjs",
                     icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://safebooru.org//images/4420/b044860fbd8ee619f9d7e637010104ad.png")
    embed.add_field(name="🪪 IW's card lv: 4", value="🌏 Earth", inline=False)
    embed.add_field(name="Status", value=ai_status.ai_stt, inline=False)
    embed.add_field(name="Mood", value=emood, inline=True)
    embed.add_field(name="Likeable", value="💖💖💖", inline=True)
    embed.add_field(name="💬 Chats", value=ai_status.total_chat, inline=True)
    embed.add_field(name="🎨 Drew", value=ai_status.total_draw, inline=True)
    embed.add_field(name="🔄️ Connected", value=ai_status.total_rcn, inline=True)
    embed.add_field(name="🕒 Time leap", value=ai_status.roll_back, inline=True)
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(map_bt)
    view.add_item(mo_bt)
    view.add_item(ha_bt)
    return embed, view

async def status_moeka():
    from utils.bot import ai_status
    async def set_emood(bot_mood):
        bot_mood = max(1, min(bot_mood, 99))
        emood_count = (bot_mood+20) // 20
        emood = "✨" * emood_count
        return emood
    
    emood = await set_emood(10)
    embed=discord.Embed(title=f"Moeka Watanabe", description="Là người làm việc với hiệu quả bất thường và độ chính xác cực cao, bạn thuở nhỏ và cùng học cao trung với Himeka. Đến từ gia tộc Watanabe nổi tiếng. Được đề cử lên làm tổng tư lệnh của IW khi 18 tuổi.", color=0xba82f2)
    embed.set_author(name="Commander-in-Chief of IWORLD", url="https://beta.character.ai/chat2?char=eNV37_ucw8ZI4SeAyuP4TD48PwaNK5-Ag4wb01D_WyY",
                     icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175795325244547072/china_moeka_high_school_fleet_drawn_by_langley1000__09f900efd1f3c96ccbab58a5bab00b02_2.png")
    embed.add_field(name="🪪 IW's card lv: S", value="🌏 Earth", inline=False)
    embed.add_field(name="Status", value="Work seriously at the IW control tower", inline=False)
    embed.add_field(name="Mood", value=emood, inline=True)
    embed.add_field(name="Likeable", value="💖", inline=True)
    embed.add_field(name="💬 Chats", value="0", inline=True)
    embed.add_field(name="🎨 Drew", value="0", inline=True)
    embed.add_field(name="🔄️ Connected", value="?", inline=True)
    embed.add_field(name="🕒 Time leap", value="?", inline=True)
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(map_bt)
    view.add_item(hi_bt)
    view.add_item(ha_bt)
    return embed, view

async def status_haruka():
    from utils.bot import ai_status, ai_full_name
    async def set_emood(bot_mood):
        bot_mood = max(1, min(bot_mood, 99))
        emood_count = (bot_mood+20) // 20
        emood = "✨" * emood_count
        return emood
    
    emood = await set_emood(24)
    embed=discord.Embed(title=f"Mizuno Haruka", description="Miêu nhân tộc đến từ thuộc địa Catalia, hầu hết dành thời gian của mình tại phòng chỉ huy của thiết giáp hạm hạng nặng Elen - tàu chiến lớn nhất thuộc Libra city.", color=0xff8a8a)
    embed.set_author(name="Captain of Elen starship", url="https://beta.character.ai/chat?char=PD_rUpadJ4d70PDJ98_zHOOEVKQ_p56R3inKPK3MhZs",
                     icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175795395792732250/portrait_white_hairband_braid_loli_pink_hair_ruby_eyes_hairclip_light_sm_s-2347311327.png")
    embed.add_field(name="🪪 IW's card lv: 3", value="😺 Catalia", inline=False)
    embed.add_field(name="Status", value="Busy on the road near Astria's asteroid belt", inline=False)
    embed.add_field(name="Mood", value=emood, inline=True)
    embed.add_field(name="Likeable", value="💖💖", inline=True)
    embed.add_field(name="💬 Chats", value="0", inline=True)
    embed.add_field(name="🎨 Drew", value="0", inline=True)
    embed.add_field(name="🔄️ Connected", value="?", inline=True)
    embed.add_field(name="🕒 Time leap", value="?", inline=True)
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(map_bt)
    view.add_item(hi_bt)
    view.add_item(mo_bt)
    return embed, view

async def status_libra():
    from utils.funcs import dot_num
    from utils.bot import ai_status
    pop = 1263865 + (ai_status.total_chat*2)
    pops = await dot_num(pop)
    bld = 1762315 + (ai_status.total_draw)
    blds = await dot_num(bld)
    vhc = int(bld/5) + int(pop/2)
    vhcs = await dot_num(vhc)
    embed=discord.Embed(title="♎ Ｌｉｂｒａ", description="Một trong 2 thành phố dân cư lớn nhất trên IW. Sở hữu mọi loại cơ sở vật chất, ẩm thực. Libra có đời sống cao, văn minh và sạch đẹp, nhiều cây xanh và luôn chào đón những khách du lịch trái đất cũng như từ các space colony khác. Tập đoàn Shindou có vốn đầu tư bất động sản lớn nhất vào thành phố này.", color=0x3db5ff)
    embed.set_author(name="Thành phố dân cư chính", url="https://beta.character.ai/chat2?char=g9qGgwr7kJRARbsOV52ChcKaEkJYPUF1A3mprJmgUjs", icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175727546130767902/Libra.png")
    embed.add_field(name=f"👨🏻‍👩 {pops} (up to 5M)", value="🪪 lv 1~4", inline=True)
    embed.add_field(name="🗺️ 820km² (up to 1200)", value="🛫 158 port", inline=True)
    embed.add_field(name=f"🌆 {blds}", value=f"🚗 {vhcs}", inline=True)
    embed.add_field(name="🕰️ 2018 -> Hiện tại", value="", inline=True)
    embed.set_footer(text="Để thăm quan Libra, cần card IW thấp nhất là lv1")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(char_bt)
    view.add_item(iw_bt)
    view.add_item(iwm_bt)
    view.add_item(iwc_bt)
    return embed, view

async def status_iw():
    from utils.funcs import dot_num
    from utils.bot import ai_status
    pop = 6638256 + (ai_status.total_chat*10)
    pops = await dot_num(pop)
    bld = 1762315 + (ai_status.total_draw)
    vhc = int(bld/3) + int(pop/2)
    embed=discord.Embed(title="🛰️ ＩＷ - Interstellar World", description="Siêu trạm vũ trụ lớn nhất từng được xây dựng bởi nhân loại, thuộc tập đoàn ISTAR và thiết kế bởi CEO của ISTAR. Khả năng tự cung cấp độc lập hoàn toàn, như một quốc gia công nghiệp kỹ thuật cao hoàn chỉnh. Các dịch vụ di chuyển công cộng trên IW đều miễn phí. Tuy không thể hạ cánh trên bất kỳ hành tinh nào nhưng IW sở hữu nhiều công nghệ động cơ tiên tiến, khiến nó gần như có thể đi tới bất kỳ đâu trong không gian sâu trong chớp mắt.", color=0x673dff)
    embed.set_author(name="Siêu trạm vũ trụ & thuộc địa không gian di động", url="https://beta.character.ai/chat2?char=eNV37_ucw8ZI4SeAyuP4TD48PwaNK5-Ag4wb01D_WyY", icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175727559422525520/IW.png")
    embed.add_field(name="Life Supports technology:", value="Hệ thống tái tạo khí quyển, trọng lực.", inline=False)
    embed.add_field(name="Engine technology:", value="Particle engine: 17, Jump/Wormhole Drive: 2", inline=False)
    embed.add_field(name="Core:", value="Plasma fusion reactor: 5, Laser reactor: 8", inline=False)
    embed.add_field(name="Weapons:", value="Super particle cannon: 1, particle cannon: 8", inline=False)
    embed.add_field(name="Shell:", value="Titanium reinforced, multi-layer force field", inline=False)
    embed.add_field(name=f"👨🏻‍👩 {pops}", value="🛫 620.156 port", inline=True)
    embed.add_field(name=f"🌍 Earth", value="🌠 150.000 LY", inline=True)
    embed.add_field(name="🗺️ 28500km²", value="🪐 200kmø", inline=True)
    embed.add_field(name="🕰️ 2018 -> Hiện tại", value="", inline=True)
    embed.set_footer(text="Có thể tới IW bằng spacecraft cá nhân hoặc thang máy vũ trụ ISKY, cần card IW thấp nhất là lv1.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(char_bt)
    view.add_item(li_bt)
    view.add_item(iwm_bt)
    view.add_item(iwc_bt)
    return embed, view

async def status_iwm():
    from utils.funcs import dot_num
    from utils.bot import ai_status
    pop = 6638256 + (ai_status.total_chat*10)
    pops = await dot_num(pop)
    bld = 1762315 + (ai_status.total_draw)
    vhc = int(bld/3) + int(pop/2)
    embed=discord.Embed(title="🛰️ ＩＷ - Map", description="IW có kiến trúc hướng trung tâm do bề ngoài hình nhẫn có các trục nối vào giữa. Các khu vực cần các lv card IW riêng để truy cập. Khu vực trọng yếu nhất là khu điều hành trung tâm (OA), duy trì toàn bộ mọi hoạt động của IW cũng như các lò phản ứng nằm bên dưới nó.", color=0x8a9dff)
    embed.set_author(name="Bản đồ cấu trúc IW", url="https://beta.character.ai/chat2?char=eNV37_ucw8ZI4SeAyuP4TD48PwaNK5-Ag4wb01D_WyY", icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175727559422525520/IW.png")
    embed.add_field(name=f"⏺️ Center", value="Operating Area (OA) - 540km²", inline=True)
    embed.add_field(name=f"🔼 North", value="Libra City - 820km²", inline=True)
    embed.add_field(name="🔽 Southern", value="Virgo City - 850km²(Under construction)", inline=True)
    embed.add_field(name="◀️ West", value="Production Area - 265km²", inline=True)
    embed.add_field(name="▶️ East", value="Factory Area - 698km²", inline=True)
    embed.add_field(name="⏹️ Below", value="Energy Area - 84km²", inline=True)
    embed.set_footer(text="Phần đáy của IW có thể kết nối với thang máy vũ trụ ISKY ở độ cao 32km.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(char_bt)
    view.add_item(li_bt)
    view.add_item(iw_bt)
    view.add_item(iwc_bt)
    return embed, view

async def status_card():
    embed=discord.Embed(title="🪪 ＩＷ's Card", description="Chứa thông tin của user như DNA, các giấy tờ tuỳ thân bằng lái xe, tài khoản ngân hàng và ví điện tử,... Không thể làm giả.", color=0x82f295)
    embed.set_author(name="Information/security card", url="https://beta.character.ai/chat2?char=eNV37_ucw8ZI4SeAyuP4TD48PwaNK5-Ag4wb01D_WyY", icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175855216063680554/IWCard.png")
    embed.add_field(name=f"🪪 lv.1: Travel", value="Thấp nhất, dành cho khách du lịch thăm quan tại Libra và Virgo. Không thể rời khỏi thành phố mà không được phép.", inline=False)
    embed.add_field(name=f"🪪 lv.2: Citizen", value="Thẻ công dân tại IW, có thẻ này sẽ được quyền sống tại các thành phố dân cư như Libra/Virgo. Có thể tham gia test bằng lái spaceship, đăng ký Space hunter.", inline=False)
    embed.add_field(name="🪪 lv.3: Work", value="Được cấp khi làm việc tại IW.", inline=False)
    embed.add_field(name="🪪 lv.4: Senior officials", value="Giám đốc các phòng ban tại IW.", inline=False)
    embed.add_field(name="🪪 lv.5: Senior Leadership", value="Làm việc tại Khu vực điều hành trung tâm (Operating Area), tháp điều khiển. Được phép truy cập hầu hết các cơ sở hạ tầng tại IW.", inline=False)
    embed.add_field(name="🪪 lv.S: Special", value="Hội đồng quản trị ISTAR, thẻ mức cao nhất cùng quyền hành cao nhất. Truy cập tất cả cơ sở hạ tầng kể cả vùng cấm hoặc tuyệt mật.", inline=False)
    embed.set_footer(text="ISTAR - Interstellar Space Tech And Research, tập đoàn vũ trụ đa quốc gia. Phát minh ra Particle engine, ISKY(toà nhà chọc trời cao 32km tích hợp thang máy vũ trụ), IW, hệ thống thẻ IW.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(char_bt)
    view.add_item(li_bt)
    view.add_item(iw_bt)
    view.add_item(iwm_bt)
    return embed, view

async def status_user(interaction, dates=None):
    from utils.bot import ai_status

    u_name = None
    u_stt = "unknown"
    if isinstance(interaction, discord.Message):
        if interaction.guild:
            u_name = interaction.author.nick
            u_stt = interaction.author.status
        uid = interaction.author.id
        u_avatar = interaction.author.avatar
        if not u_name:
            u_name = interaction.author.name
    else:
        if interaction.guild:
            u_name = interaction.user.nick
            u_stt = interaction.user.status
        uid = interaction.user.id
        u_avatar = interaction.user.avatar
        if not u_name:
            u_name = interaction.user.name

    u_stt = str(u_stt)
    if u_stt == "online":
        u_stt = "online     🟢"
    elif u_stt == "offline":
        u_stt = "offline    ⚫"
    elif u_stt == "dnd":
        u_stt = "dnd    🔴"
    elif u_stt == "idle":
        u_stt = "idle   🌙"


    u = UserData(uid)
    fr = UFrom()
    ho = UHome()
    lo = ULore()
    await u.get()
    await u.set('u_name', u_name)
    if dates and u.u_joindate == 0:
        await u.set('u_joindate', dates)
    
    async def set_emood(bot_mood):
        bot_mood = max(1, min(bot_mood, 99))
        emood_count = (bot_mood+1) // 2
        emood = "💠" * emood_count
        return emood
    
    ufrom = u.u_from
    uhome = u.u_home
    if not ufrom:
        ufrom = "unregistered"
    else:
        ufrom = await fr.get(ufrom)
    uhome = u.u_home
    if not uhome:
        uhome = "unregistered"
    else:
        uhome = await ho.get(uhome)
    ulv = u.u_lv
    lore = await lo.get(ulv)
    emood = await set_emood(ai_status.bot_mood)
    embed=discord.Embed(title=f"{u.u_name} ➖ {u_stt}", description=f"{lore}", color=0x3db5ff)
    embed.set_author(name=f"{u.u_achv}", url=u_avatar,
                     icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url=u_avatar)
    embed.add_field(name=f"🪪 IW's card lv: {ulv}", value="\u200b", inline=False)
    embed.add_field(name=f"👑 {u.u_fame} CP", value=f"🪙 {u.u_blc} IRA", inline=True)
    embed.add_field(name=f"Home: {uhome}", value=f"From: {ufrom}", inline=True)
    embed.add_field(name=f"\u200b", value="", inline=False)
    embed.add_field(name=f"💠💠🔹🔹🔹", value="", inline=False)
    embed.add_field(name=f"", value=f"🕰️ {u.u_joindate}", inline=False)
    embed.set_footer(text="IW's Card dùng để truy cập các tiện ích tại IW, cũng như là định danh, ví điện tử của riêng bạn.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(uet_bt)
    view.add_item(uwh_bt)
    return embed, view

async def status_tech(interaction):
    from utils.funcs import dot_num
    u_name = None
    if isinstance(interaction, discord.Message):
        if interaction.guild:
            u_name = interaction.author.nick
        uid = interaction.author.id
        u_avatar = interaction.author.avatar
        if not u_name:
            u_name = interaction.author.name
    else:
        if interaction.guild:
            u_name = interaction.user.nick
        uid = interaction.user.id
        u_avatar = interaction.user.avatar
        if not u_name:
            u_name = interaction.user.name

    u = UserData(uid)
    await u.get()
    await u.set('u_name', u_name)

    embed=discord.Embed(title="Equipment technology", description="Các thiết bị hiện tại của bạn.", color=0x9ea1ff)
    embed.set_author(name=u_name, icon_url=u_avatar)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175855216063680554/IWCard.png")
    #embed.add_field(name=f"\u200b", value="", inline=False)
    embed.add_field(name=f"\u200b", value="💠 **Technical Stats**", inline=False)
    spd = await dot_num(u.u_speed_st)
    embed.add_field(name=f"**•**    Speed: {spd}", value="", inline=False)
    skl = await dot_num(u.u_skl_st)
    embed.add_field(name=f"**•**    Skillful: {skl}", value="", inline=False)
    tech = await dot_num(u.u_tech_st)
    embed.add_field(name=f"**•**    Tech: {tech}", value="\u200b", inline=False)
    embed.add_field(name="1 - Empty 🟦", value="", inline=True)
    embed.add_field(name="2 - Empty 🟦", value="", inline=True)
    embed.add_field(name="3 - Empty 🟦", value="", inline=True)
    embed.add_field(name="4 - Empty 🟦", value="", inline=True)
    embed.add_field(name="5 - Empty 🟦", value="", inline=True)
    embed.add_field(name="6 - Empty 🟦", value="", inline=True)
    embed.add_field(name=f"\u200b", value="", inline=False)
    embed.set_footer(text="Các thiết bị sẽ cải thiện đáng kể chỉ số của bạn, có thể mở rộng slot trong Tech Store.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(usc_bt)
    view.add_item(uwh_bt)
    return embed, view

async def status_warehouse(interaction):
    u_name = None
    if isinstance(interaction, discord.Message):
        if interaction.guild:
            u_name = interaction.author.nick
        uid = interaction.author.id
        u_avatar = interaction.author.avatar
        if not u_name:
            u_name = interaction.author.name
    else:
        if interaction.guild:
            u_name = interaction.user.nick
        uid = interaction.user.id
        u_avatar = interaction.user.avatar
        if not u_name:
            u_name = interaction.user.name

    ie = UItem()
    u = UserData(uid)
    await u.get()
    await u.set('u_name', u_name)
    items = await u.get_item()

    embed=discord.Embed(title="Storage", description="Kho chứa item", color=0x9ea1ff)
    embed.set_author(name=u_name, icon_url=u_avatar)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1096933532032581693/1175855216063680554/IWCard.png")
    embed.add_field(name=f"\u200b", value="", inline=False)

    # Iterate through items and add 'Name' and 'qtt' to the embed
    for item in items:
        item_id = item['id']
        item_info = await ie.get(item_id)
        if item_info:
            item_name = item_info.get('Name', 'Unknown')  # Replace 'Unknown' with a default value if 'Name' is not found
        else:
            item_name = "Unknown"
        item_qtt = item['qtt']

        field_name = f"{item_name} ({item_qtt})"
        embed.add_field(name=field_name, value="", inline=True)

    embed.add_field(name=f"\u200b", value="", inline=False)
    embed.set_footer(text="Sức chứa tuỳ vào spacecraft bạn đang sở hữu, có thể mở rộng sức chứa tối đa.")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    view.add_item(usc_bt)
    view.add_item(uet_bt)
    return embed, view

#embed.add_field(name="🟩 1", value="🟩 2", inline=True)

async def item_show(id=None, name=None, type=None, lore=None, consum=None, stack=None, sell=None, lv=None, cp=None, spd=None, skl=None, tech=None, uid=None, uname=None, rare=None, icon = None):
    from utils.bot import item
    from utils.funcs import dot_num
    from utils.user_data import UserData, UItem
    if id:
        list = await item.get(id=id)
    if name:
        list = await item.get(name=name)
    if not name or not id:
        id = list['ID']
        name = list['Name']
        type = list['Type']
        lore= list['Lore']
        consum= list['Consumable']
        stack= list['Stackable']
        sell= list['Sellable']
        lv= list['Level']
        cp= list['CP']
        spd= list['Spd']
        skl= list['Skl']
        tech= list['Tech']
        rare= list['Rare']
        icon = list['icon']

    if "raw" in type:
        type = "💎 Nguyên liệu"
    elif "materials" in type:
        type = "🧱 Vật liệu"
    elif "components" in type:
        type = "⚙️ Linh kiện"
    elif "tech" in type:
        type = "📡 Thiết bị"
    elif "food" in type:
        type = "🍱 Nhu yếu phẩm"
    elif "special" in type:
        type = "🎖️ Đặc biệt"

    trare = ""
    if rare:
        rare = int(rare)
        if rare == 1:
            rare = "⬜"
            trare = "Common"
        elif rare == 2:
            rare = "🟩"
            trare = "Uncommon"
        elif rare == 3:
            rare = "🟦"
            trare = "Rare"
        elif rare == 4:
            rare = "🟪"
            trare = "Epic"
        elif rare == 5:
            rare = "🟨"
            trare = "Legendary"
        elif rare == 6:
            rare = "🟥"
            trare = "Artifact"
    qtt = 0
    if uid:
        udt = UserData(uid)
        await udt.get()
        items = udt.items
        ie = None  # Khởi tạo ie là None
        for item in items:
            if id == item['id']:  # So sánh iid với id của từng phần tử
                ie = item
                break
        if ie:
            qtt = ie['qtt']
    
    embed=discord.Embed(title=f"{name}", description=lore, color=0x9ea1ff)
    embed.set_author(name=f"ID: #{id}", icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    embed.set_thumbnail(url=icon)

    embed.add_field(name="\u200b", value=f"**{type}**", inline=False)
    embed.add_field(name=f"{rare} Độ hiếm: {trare}", value=f"", inline=False)
    if sell and int(sell) > 0:
        sell = await dot_num(sell)
        embed.add_field(name=f"**•**    Giá: {sell} Ira", value="\u200b", inline=False)
    if consum and float(consum) > 0:
        consum = await dot_num(consum)
        embed.add_field(name=f"**•**    Số lần dùng: {consum}", value="", inline=False)
    if stack and int(stack) > 1:
        embed.add_field(name=f"**•**    Có thể xếp chồng: {stack}", value="", inline=False)

    if spd or spd != 0 or skl or skl != 0 or tech or tech != 0:
        embed.add_field(name=f"\u200b", value="💠 **Technical**", inline=False)
    if spd or spd != 0:
        spd = await dot_num(spd)
        embed.add_field(name=f"**•**    Speed: +{spd}", value="", inline=False)
    if skl or skl != 0:
        skl = await dot_num(skl)
        embed.add_field(name=f"**•**    Skillful: +{skl}", value="", inline=False)
    if tech or tech != 0:
        tech = await dot_num(tech)
        embed.add_field(name=f"**•**    Tech: +{tech}", value="", inline=False)
    
    if lv and lv != 1 or cp or cp != 0:
        embed.add_field(name=f"\u200b", value="🪪 **Requirements**", inline=False)
    if lv and lv != 1:
        embed.add_field(name=f"**•**    IW's card lv: {lv}", value="", inline=False)
    if cp or cp != 0:
        cp = await dot_num(cp)
        embed.add_field(name=f"**•**    Danh vọng: {cp} CP", value="", inline=False)
    if qtt and uname:
        embed.set_footer(text=f"{uname} đang có: {qtt}")
    view = View(timeout=None)
    view.add_item(irmv_bt)
    return embed, view

async def rena_notice(answ=None, uname=None):
    embed=discord.Embed(title="📑 Himeka đang bận", description="Himeka đang bận hoặc kết nối không ổn định, thử ấn nút `reconnect`, đợi 20s rồi gọi lại cô ấy.", color=0xffbf75)
    if "sleep" in answ:
        embed=discord.Embed(title="Himeka đang ngủ 💤", description="Đợi tới sáng hoặc gọi cô ấy dậy.", color=0xffbf75)
    embed.set_author(name="Rena - Himeka's tablet", url="https://beta.character.ai/chat2?char=g9qGgwr7kJRARbsOV52ChcKaEkJYPUF1A3mprJmgUjs", icon_url="https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png")
    return embed