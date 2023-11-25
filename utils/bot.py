import asyncio, json, os, random, discord, time, datetime, re, logging
from discord.ext import commands, tasks
from discord.ui import View, button

from user_files.config import *
from utils.ai_api import *
from utils.funcs import *
from utils.buttons import *
from utils.daily import *
from utils.status import *
from utils.user_data import *

logging.getLogger('discord.gateway').setLevel(logging.ERROR)

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

bot.load_extension("speech.speech_cog")
# Configuration of speech logger
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("speech.speech_cog")
logger.setLevel(logging.WARNING)

emojis = []

class AllStatus:
    def __init__(self):
        # Status
        self.total_chat = 0
        self.roll_back = 0
        self.bot_mood = 50
        self.total_draw = 0
        self.total_rcn = 0
        self.total_tl = 0
        self.chat_log = False
        self.cds_log = True
        self.st_log = False
        self.igen_flw = False
        self.img_prompt = "sky"
        self.img_dprt = "sea"
        self.iregen = False
        self.pr_ch_id = 0
        self.pr_vch_id = 0
        self.last_user = "Shiro"
        self.u_in_vc = []
        self.ai_stt = "Chilling ✨"
        self.day_time = False
        self.non_time = False
        self.atn_time = False
        self.night_time = False
        self.ai_busy = False
        self.sleep_cd = -1
        self.sleep_rd = False
        self.sleeping = False
        self.bot_ivd = False
        self.rt_c = 0
        self.bot_cls = 0
        self.chat_channel = 0
        self.char_id = None

    async def update(self, val_name, value):
        if hasattr(self, val_name):
            current_value = getattr(self, val_name)
            setattr(self, val_name, current_value + value)
            await vals_save("user_files/vals.json", val_name, current_value + value)
        else:
            print(f"Error: Variable '{val_name}' not found.")

    async def set(self, val_name, value):
        if hasattr(self, val_name):
            setattr(self, val_name, value)
            await vals_save("user_files/vals.json", val_name, value)
        else:
            print(f"Error: Variable '{val_name}' not found.")

    async def get(self, val_name):
        if hasattr(self, val_name):
            value = getattr(self, val_name)
        return value
    
    async def load(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            for variable_name, value in data.items():
                if hasattr(self, variable_name):
                    setattr(self, variable_name, value)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error loading data from {filename}")

    async def show(self):
        for attr, value in vars(self).items():
            print(f"[vals.json] - {attr}: {value}")

ai_status = AllStatus()
item = UItem()

# AI name
ai_name = "Himeka"
ai_last = "Shindou"
tablet_name = "Rena"
gui_name = "NekoArt Studio"
ai_full_name = f"{ai_name} {ai_last}"

# Image gen
igen_lists = {}
ihq = False
iquality = "standard"
iportrait = False
iscene = False
isize = "1024x1024"

@bot.event
async def on_ready():
    global emojis
    # Load vals
    await ai_status.load('user_files/vals.json')
    
    # get emojis
    guild = bot.get_guild(server_id)
    emojis = guild.emojis

    # Emojis load
    emojis_take(bot)

    # Load button
    await load_btt()

    # Time circle
    asyncio.create_task(m_check())
    m_check.start()

    asyncio.create_task(h_check())
    h_check.start()

    # Load status
    await status_change()

    print(f"{ai_name} đã khởi động")
    
    # Continue voice
    await voice_rcn()

    # Continue draw
    if ai_status.iregen:
        umess = f"Your tablet: You are continuing to draw for {ai_status.last_user}"
        message = await mess_id_send(bot, ai_status.pr_ch_id, umess, ai_status.chat_log)
        asyncio.create_task(img_gen(message, ai_status.img_prompt, iquality, isize))

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return
    bot_voice_channel = bot.voice_clients[0].channel if bot.voice_clients else None
    if after.channel == bot_voice_channel and after.channel is not None and before.channel is None:
        if member.name not in user_timers:
            uid = member.id
            user_timers[member.name] = 1800
            asyncio.create_task(count_down(user_timers, member.name))
            umess = (f"Your tablet: {member.name} joined voice channel '{bot_voice_channel.name}' with you")
            asyncio.create_task(mess_id_send(bot, ai_status.pr_ch_id, umess, ai_status.chat_log))
            u = UserData(uid)
            await u.update('u_fame', 1)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.content.startswith((".", "<", "!", ",", "/")):
        return
    if ai_status.chat_channel != 0:
        if message.channel.id != ai_status.chat_channel:
            return
    # Phản hồi chat
    if message.content:
        if ai_status.bot_ivd:
            await ai_status.set('bot_ivd', False)
        if ai_status.sleep_rd:
            await ai_status.set('sleep_cd', 3)
        user_name = message.author.nick
        if not user_name:
            user_name = message.author.name
        mess = message.content
        asyncio.create_task(mess_rep(message, mess, user_name, ai_status.chat_log))

# Image gen dall e 3 in chat
async def img_gen_chat(message, result):
    global iquality, isize
    igen_flw = ai_status.igen_flw
    img_prompt = ai_status.img_prompt
    async def igen_choice(text):
        quality = None
        size = None
        if re.search(r'quality|sharp|chất|hq|hd', text, re.IGNORECASE):
            quality = "hd"
        if re.search(r'dung|portrait', text, re.IGNORECASE):
            size = "1024x1792"
        if re.search(r'cảnh|scene', text, re.IGNORECASE):
            size = "1792x1024"
        if not quality:
            quality = iquality
        if not size:
            size = isize
        return quality, size
    if not igen_flw:
        if re.search(r'gen|create|tạo|vẽ|draw|chụp|made', result, re.IGNORECASE) and re.search(r'art|img|pic|ảnh|hình|tấm', result, re.IGNORECASE) and not re.search(r'lại|nữa|again|more', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            iquality = quality
            isize = size
            lang = "en"
            translated = text_translate(result, lang)
            prompt = extract_nouns(translated)
            img_prompt = prompt
            await ai_status.set('img_prompt', prompt)
            await img_gen(message, prompt, quality, size)
            return
        elif re.search(r'gen|create|tạo|vẽ|draw|chụp|made', result, re.IGNORECASE) and re.search(r'art|img|pic|ảnh|hình|tấm', result, re.IGNORECASE) and re.search(r'lại|nữa|again|more', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            await img_gen(message, img_prompt, quality, size)
            return
    else:
        # Gen thêm lần nữa
        if re.search(r'lại|again|lần', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            await img_gen(message, img_prompt, quality, size)
            return
        # Gen giống như art đã gen
        elif re.search(r'next|more|tiếp|giống|similar|tự|như|like|same', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            await img_gen(message, img_dprt, quality, size)
            return
        # Sửa lại prompt và gen thêm
        elif re.search(r'sửa|fix|chuyển|change|đổi|thay|thêm|add|qua|chọn|lấy|choose|take', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            lang = "en"
            translated = text_translate(result, lang)
            prompt = extract_nouns(translated)
            await img_regen(message, quality, size, prompt)
            return
        elif re.search(r'gen|create|tạo|vẽ|draw|chụp|photo|image|img', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            iquality = quality
            isize = size
            lang = "en"
            translated = text_translate(result, lang)
            prompt = extract_nouns(translated)
            await ai_status.set('img_prompt', prompt)
            await img_gen(message, prompt, quality, size)
            return
        else:
            igen_flw = False
            await ai_status.set('igen_flw', igen_flw)
                    
# Image gen dall e 3
async def img_gen(interaction, prompt, quality, size):
    global igen_lists
    igen_flw = ai_status.igen_flw
    img_dprt = ai_status.img_dprt
    iregen = ai_status.iregen

    emoji = random.choice(emojis)

    user_nick = None
    uid = None
    if isinstance(interaction, discord.Message):
        user_nick = interaction.author.nick
        uid = interaction.author.id
        if not user_nick:
            user_nick = interaction.author.name
    else:
        user_nick = interaction.user.nick
        uid = interaction.user.id
        if not user_nick:
            user_nick = interaction.user.name
    
    if ai_status.cds_log:
        print(f"[IMG GENERATE] - {user_nick}")
        print()
    artist = ai_name
    if ai_status.sleeping or ai_status.ai_busy:
        artist = tablet_name
    embed = discord.Embed(title=f"{artist} đang vẽ cho {user_nick}... {emoji}", description=f"🏷️ {prompt}", color=0xffbf75)
    view = View(timeout=None)
    view.add_item(irmv_bt)
    if isinstance(interaction, discord.Message):
        await interaction.channel.send(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view)

    async for message in interaction.channel.history(limit=1):
        img_id = message.id
    r_prompt = prompt
    view.add_item(rg_bt)
    img = None
    eimg = None
    errar = None
    error_code = None
    try:
        img, r_prompt = await openai_images(prompt, quality, size)
        view.add_item(rgs_bt)
    except Exception as e:
        if hasattr(e, 'response') and hasattr(e.response, 'json') and 'error' in e.response.json():
            error_message = e.response.json()['error']['message']
            error_code = e.response.json()['error']['code']
            print(f"Error while gen art: {error_code} - {error_message}")
            error_message = error_message[:250]
            if error_code != 502:
                if "content_policy_violation" in error_code:
                    error_code = "Prompt không an toàn... つ﹏⊂"
                    errar = f"Your tablet: *Error* What you're drawing is a bit inappropriate."
                elif "rate_limit_exceeded" in error_code:
                    error_code = "Đợi 1 phút nữa nhé... ≧﹏≦"
                    errar = f"Your tablet: *freeze* {user_nick} asks you to draw too fast causing the tablet to freeze, tell them to wait."
                elif "billing_hard_limit_reached" in error_code:
                    error_code = "Hết cá ròi... 〒▽〒"
                    errar = "Your tablet: *Out of battery*"
            else:
                error_code = "Ah, lỗi gì vậy ta? (ˉ▽ˉ；)..."
                errar = "Your tablet: Software error while drawing, try restarting your drawing app."
        else:
            error_code = str(e)
            error_code = error_code[:250]
            error_message = error_code[:250]
            if "Connection error" in error_code:
                error_code = "Lỗi kết nối... (ˉ﹃ˉ)"
                errar = "Your tablet: Software error while drawing, try restarting your drawing app."
                await ai_status.update('bot_cls', 1)
                if ai_status.bot_cls == 2:
                    error_code = f"{ai_name} khởi động lại tablet xíu nha... (✿◠‿◠)"
                    error_message = "Sẽ quay lại liền nè~!"
                    errar = f"Your tablet: *Error error* Please ask {user_nick} to wait while restart your tablet."
            if not error_code:
                error_code = f"Lỗi gì đó mà {ai_name} cũng hem biết là lỗi gì... ∑( 口 ||"
                errar = f"Your tablet: An unknown error occurred and your drawing file was lost. Please redraw."
            print(f"Error while gen art: {e}")
    igen_lists[img_id] = {"prompt": prompt, "r_prompt": r_prompt, "quality": quality, "size": size}
    if quality == "hd":
        quality = "High Quality"
    if quality == "standard":
        quality = "Standard"
    if img:
    # Tạo một Embed để gửi hình ảnh
        embed = discord.Embed(description=f"🏷️ {prompt}", color=0xffbf75)
        embed.add_field(name=f"🌸 {quality}       🖼️ {size}", value="", inline=False)
        embed.set_image(url=img)
    else:
        eimg = [
            "https://safebooru.org//images/4262/6985078225c8f12e9054220ab6717df7c1755077.png",
            "https://safebooru.org//images/3760/35bfbabb44813b36749c96a17b0a1fb1f59eeb8e.jpg",
            "https://safebooru.org//images/3362/c3e6557a11032bcb4aed7840285f98feee136094.png"
        ]
        eimg = random.choice(eimg)
        embed = discord.Embed(description=f"🏷️ {prompt}", color=discord.Color.blue())
        embed.add_field(name=f"❌ {error_code}", value=f"_{error_message}_", inline=False)
        embed.set_image(url=eimg)
    # Gửi embed lên kênh
    async for message in interaction.channel.history(limit=10):
        if message.id == img_id:
            await message.edit(embed=embed, view=view)
            break
    if img:
        botid = bot.user.id
        b = UserData(botid)
        await b.update('u_fame', 5)
        u = UserData(uid)
        await u.update('u_fame', 1)
        if not igen_flw:
            img_dprt = r_prompt
            await ai_status.set('img_dprt', img_dprt)
        await dl_img(img, img_id)
        file_path = f'user_files/gen_imgs/{img_id}.png'
        r,g,b = await img_get_color(file_path)
        embed = discord.Embed(description=f"🏷️ {prompt}", color=discord.Colour.from_rgb(r,g,b))
        embed.add_field(name=f"🌸 {quality}       🖼️ {size}", value="", inline=False)
        image_file = discord.File(file_path, filename=f"{img_id}.png")
        embed.set_image(url=f"attachment://{image_file.filename}")
        await message.edit(embed=embed, view=view, files=[image_file])

        os.remove(file_path)

    if img or eimg:
        igen_flw = True
        await ai_status.set('igen_flw', igen_flw)
    if eimg:
        await mess_send(message, errar, ai_status.chat_log)
    await ai_status.update('bot_mood', 1)
    await ai_status.update('total_draw', 1)
    if error_code:
        if "nối" in error_code or "hem" in error_code or "vậy" in error_code:
            await img_gen(message, ai_status.img_prompt, iquality, isize)
    if ai_status.bot_cls == 2:
        iregen = True
        pr_ch_id = message.channel.id
        last_user = user_nick
        await ai_status.set('iregen', iregen)
        await ai_status.set('pr_ch_id', pr_ch_id)
        await ai_status.set('last_user', last_user)
        await ai_status.set('bot_cls', 0)
        await bot.close()
    iregen = False
    await ai_status.set('iregen', iregen)
    return

# Correct prompt and gen art again
async def img_regen(message, quality, size, rq):
    case = f"3[{ai_status.img_dprt}][{rq}]"
    try:
        prompt = await openai_task(case)
    except Exception as e:
        e = str(e)
        print("Error while correct img prompt: ", e)
        return
    await img_gen(message, prompt, quality, size)

# Các câu lệnh
@bot.slash_command(name="igen", description=f"Tạo art")
async def image_gen(interaction: discord.Interaction, prompt: str = None, hq: bool = ihq, portrait: bool = iportrait, scene: bool = iscene):
    if interaction.guild is None:
        return await interaction.response.send_message(f"{ai_name}'s tablet: {ai_name} chỉ có thể vẽ cho bạn trong {gui_name}.", ephemeral=True)
    global ihq, iportrait, iscene
    if not prompt:
        prompt = ai_status.img_prompt
    ihq = hq
    iportrait = portrait
    iscene = scene
    quality = "standard"
    size = "1024x1024"
    if hq:
        quality = "hd"
    if portrait:
        size = "1024x1792"
    if scene:
        size = "1792x1024"
    await ai_status.set('img_prompt', prompt)
    await img_gen(interaction, prompt, quality, size)

@bot.slash_command(name="reconnect", description=f"Kết nối lại với {ai_name}.")
async def renew(interaction: discord.Interaction):
    if interaction.guild is None:
        return await interaction.response.send_message(f"{ai_name}'s tablet: bạn đang ở ngoài {gui_name}.", ephemeral=True)
    await interaction.response.send_message(f"{ai_name}'s tablet: *đang thiết lập lại kết nối giữa {gui_name} với {ai_name}*", ephemeral=True)
    await ai_status.update('total_rcn', 1)
    await bot.close()

@bot.slash_command(name="timeleap", description=f"Gặp {ai_name} ở timeline khác.")
async def newchat(interaction: discord.Interaction):
    if interaction.guild is None:
        return await interaction.response.send_message(f"{ai_name}'s tablet: {ai_name} chưa từng tiếp xúc với bạn ở đây.", ephemeral=True)
    iuser = interaction.user.name
    if ai_status.rt_c == 0:
        await interaction.response.send_message(f"{ai_name}'s tablet: Hành động này không thể undo, {iuser} chắc chứ?", ephemeral=True)
        await ai_status.update('rt_c', 1)
    else:
        await interaction.response.send_message(f"*Đã quay ngược thời gian lúc {ai_name} mới tham gia NekoArt Studio... 🕒*")
        await CAc.chat.new_chat(c_token)
        await ai_status.set('bot_mood', 50)
        await ai_status.update('roll_back', 1)
        await ai_status.set('rt_c', 0)
        if ai_status.cds_log:
            print(f"[NEW CHAT] - {iuser}")
            print()

@bot.slash_command(name="status", description=f"{ai_name} tablet")
async def status_show(interaction: discord.Interaction):
    embed, view = await status_himeka()
    await interaction.response.send_message(embed=embed, view=view)

@bot.slash_command(name="uinfo", description=f"Thông tin cá nhân của bạn.")
async def u_status_show(interaction: discord.Interaction):
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)
    date = vn_time.date()
    hour = vn_time.hour
    m = vn_time.minute
    dates = f"{date} {hour}:{m}"
    embed, view = await status_user(interaction, dates)
    await interaction.response.send_message(embed=embed, view=view)

@bot.slash_command(name="clogs", description=f"Nhật ký của {ai_name}")
async def cslog(interaction: discord.Interaction, chat: bool = False, command: bool = True, status: bool = False, get: str = None):
    if interaction.user.id == dev_id:
        if get:
            val = await ai_status.get(get)
            await interaction.response.send_message(f"{val}", ephemeral=True)
        else:
            await ai_status.set('chat_log', chat)
            await ai_status.set('cds_log', command)
            await ai_status.set('st_log', status)
            await interaction.response.send_message(f"`Chat log: {chat}, Command log: {command}, Status log: {status}.`", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name} mới có thể xem nhật ký của cô ấy.`", ephemeral=True)

@bot.slash_command(name="tablet", description=f"{ai_name} tablet")
async def test_cmd(interaction: discord.Interaction):
    if interaction.user.id == dev_id:
        await interaction.response.send_message(f"Pong~!", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name} mới có thể mở tablet của cô ấy.`", ephemeral=True)

@bot.slash_command(name="chat_channel", description=f"Đổi chat channel cho {ai_name}.")
async def chat_channel_change(interaction: discord.Interaction, chat_channel: str = "0"):
    if interaction.user.id == dev_id:
        if not chat_channel == "0":
            channel = bot.get_channel(int(chat_channel))
            if channel:
                await ai_status.set('chat_channel', int(chat_channel))
                await interaction.response.send_message(f"{ai_name} sẽ chat với mọi người tại **{channel.name}**.", ephemeral=True)
            else:
                await interaction.response.send_message(f"ID của channel không hợp lệ.", ephemeral=True)
        else:
            await ai_status.set('chat_channel', 0)
            await interaction.response.send_message(f"{ai_name} sẽ chat với mọi người trên tất cả chat channel được cấp role.", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name} mới có thể mở tablet của cô ấy.`", ephemeral=True)

@bot.slash_command(name="cchar", description=f"Đổi character.")
async def character_change(interaction: discord.Interaction, char_id: str = None):
    if interaction.user.id == dev_id:
        if char_id:
                await ai_status.set('char_id', char_id)
                await interaction.response.send_message(f"Đã đổi nhân vật thành công.", ephemeral=True)
        else:
            await ai_status.set('char_id', char_id)
            await interaction.response.send_message(f"Character sẽ là {ai_name}.", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name} mới có thể mở tablet của cô ấy.`", ephemeral=True)

@bot.slash_command(name="add_item", description=f"Thêm item cho {ai_name}, DEV-only")
async def item_add(interaction: discord.Interaction,
                    name: str,
                    type: discord.Option(
        description="Loại item",
        choices=[
            discord.OptionChoice(name="nguyên liệu thô", value="raw"),
            discord.OptionChoice(name="vật liệu", value="materials"),
            discord.OptionChoice(name="thành phần/Linh kiện", value="components"),
            discord.OptionChoice(name="thiết bị", value="tech"),
            discord.OptionChoice(name="nhu yếu phẩm", value="food"),
            discord.OptionChoice(name="đặc biệt", value="special"),
        ],
    ) = "raw",
                    lore: str="item có thể sử dụng tại IW",
                    consum: int=0,
                    stack: discord.Option(
        description="Kích thước - khả năng xếp chồng",
        choices=[
            discord.OptionChoice(name="1"),
            discord.OptionChoice(name="8"),
            discord.OptionChoice(name="16"),
            discord.OptionChoice(name="32"),
            discord.OptionChoice(name="64"),
            discord.OptionChoice(name="128"),
            discord.OptionChoice(name="512"),
        ],
    ) = 0,
                    sell: int=0,
                    lv: discord.Option(
        description="Yêu cầu IW's card lv",
        choices=[
            discord.OptionChoice(name="1"),
            discord.OptionChoice(name="2"),
            discord.OptionChoice(name="3"),
            discord.OptionChoice(name="4"),
            discord.OptionChoice(name="5"),
            discord.OptionChoice(name="6"),
        ],
    ) = 1,
                    cp: int=0,
                    spd: int=0,
                    skl: int=0,
                    tech: int=0,
                    rare: discord.Option(
        description="Độ hiếm",
        choices=[
            discord.OptionChoice(name="Common", value="1"),
            discord.OptionChoice(name="Uncommon", value="2"),
            discord.OptionChoice(name="Rare", value="3"),
            discord.OptionChoice(name="Epic", value="4"),
            discord.OptionChoice(name="Legendary", value="5"),
            discord.OptionChoice(name="Artifact", value="6"),
        ],
    ) = "1",
    icon: str = "https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png"):

    uid = interaction.user.id
    uname = interaction.user.nick
    if not uname:
        uname = interaction.user.name
    await item.set(name, type, spd, skl, tech, lore, stack, consum, sell, lv, cp, rare, icon)
    ie = await item.get(name=name)
    if ie:
        itd =  ie["ID"]
    embed, view = await item_show(id=itd, uid=uid, uname=uname)
    await interaction.response.send_message(embed=embed, view=view)

@bot.slash_command(name="edit_item", description="Sửa item, DEV-only")
async def item_edit(interaction: discord.Interaction,
                      id: int,
                      name: str = None,
                      type: discord.Option(
        description="Loại item",
        choices=[
            discord.OptionChoice(name="nguyên liệu thô", value="raw"),
            discord.OptionChoice(name="vật liệu", value="materials"),
            discord.OptionChoice(name="thành phần/Linh kiện", value="components"),
            discord.OptionChoice(name="thiết bị", value="tech"),
            discord.OptionChoice(name="nhu yếu phẩm", value="food"),
            discord.OptionChoice(name="đặc biệt", value="special"),
        ],
    ) = None,
                      lore: str = None,
                      consum: int = None,
                      stack: discord.Option(
        description="Kích thước - khả năng xếp chồng",
        choices=[
            discord.OptionChoice(name="1"),
            discord.OptionChoice(name="8"),
            discord.OptionChoice(name="16"),
            discord.OptionChoice(name="32"),
            discord.OptionChoice(name="64"),
            discord.OptionChoice(name="128"),
            discord.OptionChoice(name="512"),
        ],
    ) = None,
                      sell: int = None,
                      lv: discord.Option(
        description="Yêu cầu IW's card lv",
        choices=[
            discord.OptionChoice(name="1"),
            discord.OptionChoice(name="2"),
            discord.OptionChoice(name="3"),
            discord.OptionChoice(name="4"),
            discord.OptionChoice(name="5"),
            discord.OptionChoice(name="6"),
        ],
    ) = None,
                      cp: int = None,
                      spd: int = None,
                      skl: int = None,
                      tech: int = None,
                    rare: discord.Option(
        description="Độ hiếm",
        choices=[
            discord.OptionChoice(name="Common", value="1"),
            discord.OptionChoice(name="Uncommon", value="2"),
            discord.OptionChoice(name="Rare", value="3"),
            discord.OptionChoice(name="Epic", value="4"),
            discord.OptionChoice(name="Legendary", value="5"),
            discord.OptionChoice(name="Artifact", value="6"),
        ],
    ) = None,
    icon: str = None):

    i = await item.get(id)
    if not i:
        await interaction.response.send_message(f"Không có item nào có id là {id}.", ephemeral=True)
        return

    update_data = {}
    
    uid = interaction.user.id
    uname = interaction.user.nick
    if not uname:
        uname = interaction.user.name
    # Kiểm tra từng biến nếu không phải là None thì thêm vào dictionary update_data
    if name is not None:
        update_data['Name'] = name
    if type is not None:
        update_data['Type'] = type
    if lore is not None:
        update_data['Lore'] = lore
    if consum is not None:
        update_data['Consumable'] = consum
    if stack is not None:
        update_data['Stackable'] = stack
    if sell is not None:
        update_data['Sellable'] = sell
    if lv is not None:
        update_data['Level'] = lv
    if cp is not None:
        update_data['CP'] = cp
    if spd is not None:
        update_data['Spd'] = spd
    if skl is not None:
        update_data['Skl'] = skl
    if tech is not None:
        update_data['Tech'] = tech
    if rare is not None:
        update_data['Rare'] = rare
    if icon is not None:
        update_data['icon'] = icon
    # Nếu có ít nhất một biến không phải là None, thì gọi hàm item.update(id) với các thông số đã cập nhật
    if update_data:
        await item.update(id, **update_data)

    embed, view = await item_show(id, uid=uid, uname=uname)
    await interaction.response.send_message(embed=embed, view=view)

@bot.slash_command(name="get_item", description=f"Lấy item, DEV-only")
async def item_get(interaction: discord.Interaction, id: int=None, name: str=None):
    uid = interaction.user.id
    uname = interaction.user.nick
    if not uname:
        uname = interaction.user.name
    i = None
    e = None
    if id:
        i = await item.get(id)
        if i:
            embed, view = await item_show(id=id, uid=uid, uname=uname)
        e = id
    elif name:
        i = await item.get(name)
        if i:
            embed, view = await item_show(name=name, uid=uid, uname=uname)
        e = name
    if not i:
        await interaction.response.send_message(f"Không có item nào có id hoặc name là {e}.", ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, view=view)

@bot.slash_command(name="edit_item_ptt", description=f"Xoá item, DEV-only")
async def item_new_ptt(interaction: discord.Interaction, command: discord.Option(
        description="Chọn cách xử lý item.",
        choices=[
            discord.OptionChoice(name="Thêm - [name, value]", value="add"),
            discord.OptionChoice(name="Xoá - [name]", value="del"),
        ]), name: str, value: str = None):
    if "add" in command:
        await item.add_ptt(name, value)
        await interaction.response.send_message(f"Thuộc tính mới {name} đã được thêm vào tất cả các item hiện tại.")
    elif "del" in command:
        await item.remove_ptt(name)
        await interaction.response.send_message(f"Thuộc tính mới {name} đã được xoá thành công cho tất cả các item hiện tại.")

@bot.slash_command(name="show_item_list", description=f"Hiện toàn bộ danh sách item theo từng type, DEV-only")
async def item_show_list(interaction: discord.Interaction, classify: discord.Option(
        description="Phân loại theo:",
        choices=[
            discord.OptionChoice(name="Loại item", value="Type"),
            discord.OptionChoice(name="Độ hiếm", value="Rare"),
            discord.OptionChoice(name="Độ xếp chồng", value="Stackable"),
            discord.OptionChoice(name="Số lần dùng", value="Consumable"),
            discord.OptionChoice(name="Giá Ira", value="Sellable"),
            discord.OptionChoice(name="IW's lv card", value="Level"),
            discord.OptionChoice(name="CP", value="CP"),
            discord.OptionChoice(name="IW's lv card", value="Level"),
            discord.OptionChoice(name="Techs - Speed", value="Spd"),
            discord.OptionChoice(name="Techs - Skillful", value="Skl"),
            discord.OptionChoice(name="Techs - Tech", value="Tech"),
        ],
    ) = "Type"):
    items = item.items

    # Sắp xếp danh sách items theo ID tăng dần
    sorted_items = sorted(items, key=lambda x: x["ID"])

    # Tạo một dict để lưu trữ item theo từng type
    items_by_type = {}

    for it in sorted_items:
        item_type = it[classify]
        if item_type not in items_by_type:
            items_by_type[item_type] = []

        items_by_type[item_type].append(f'{it["ID"]}:    {it["Name"]}\n')

    # Tạo danh sách item dưới dạng "type": "id1: name1, id2: name2, ..."
    items_list = [f'**{item_type}:**\n{"".join(items)}' for item_type, items in items_by_type.items()]

    # Ghép các phần tử của danh sách thành một chuỗi, mỗi item type trên một dòng
    items_str = '\n'.join(items_list)

    # Kiểm tra nếu items_str không chứa giá trị
    if not items_str.strip():
        await interaction.response.send_message("Danh sách item trống.", ephemeral=True)
    else:
        await interaction.response.send_message(content=items_str)

@bot.slash_command(name="remove_item", description=f"Xoá item, DEV-only")
async def item_delete(interaction: discord.Interaction, id: int):
    i = await item.get(id)
    if not i:
        await interaction.response.send_message(f"Không có item nào có id là {id}.")
        return
    iname = i['Name']
    await item.delete(id)
    await interaction.response.send_message(f"Item {id} có tên '{iname}' đã bị xoá.")

@bot.slash_command(name="user_item", description=f"Quản lý item của user, DEV-only")
async def user_item(interaction: discord.Interaction, command: discord.Option(
        description="Chọn cách xử lý item.",
        choices=[
            discord.OptionChoice(name="Thêm - [iid, quantity(optional), consum(optional)]", value="add"),
            discord.OptionChoice(name="Cập nhật - [index, quantity, sell(optional)]", value="update"),
            discord.OptionChoice(name="Hiển thị - [index]", value="get"),
            discord.OptionChoice(name="Xoá - [index]", value="remove"),
        ]),
        iid: discord.Option(int,
        description="#ID của item.") = -1,
        index: discord.Option(int,
        description="Số thứ tự item đó trong Storage của user.") = 0,
        quantity: discord.Option(float,
        description="Số lượng item cần thay đổi.") = 0,
        consum: discord.Option(float,
        description="Item đó có thể sử dụng bao nhiêu lần? Có thể dùng: > 0, để trống = mặc định") = None,
        sell: discord.Option(bool,
        description="Khi chọn 'cập nhật' và giảm số lượng item, 'sell' sẽ giúp bỏ qua 'consum'.") = False):
    
    uid = interaction.user.id
    u = UserData(uid)
    noti = None
    no = None
    if index:
        index = int(index) - 1
    if quantity:
        quantity = float(quantity)
    if consum:
        consum = int(consum)
    print(index, ", ", quantity)
    if "add" in command:
        noti = await u.add_item(iid, quantity, consum)
        embed, view = await status_warehouse(interaction)
    elif "update" in command:
        noti = await u.update_item(index, quantity, sell)
        embed, view = await status_warehouse(interaction)
    elif "get" in command:
        no = await u.get_item(index)
        if no:
            iid = no['id']
            embed, view = await item_show(iid)
        else:
            noti = "Sai vị trí item."
    elif "remove" in command:
        await u.get()
        noti = await u.remove_item(index)
        embed, view = await status_warehouse(interaction)
    if not noti and not no:
        await interaction.response.send_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(f"{noti}", ephemeral=True)

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    bot_run()