import asyncio, json, os, random, discord, time, datetime, re, logging
from discord.ext import commands, tasks
from discord.ui import View, button

from user_files.config import *
from utils.ai_api import *
from utils.funcs import *
from utils.buttons import *

logging.getLogger('discord.gateway').setLevel(logging.ERROR)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class AllStatus:
    def __init__(self):
        # Status
        self.total_chat = 0
        self.roll_back = 0
        self.bot_mood = 50
        self.total_draw = 0
        self.chat_log = False
        self.cds_log = True
        self.st_log = False
        self.igen_flw = False
        self.img_prompt = "sky"
        self.img_dprt = "sea"
        self.iregen = False
        self.pr_ch_id = 0
        self.last_user = "Shiro"

    def update(self, val_name, value):
        if hasattr(self, val_name):
            current_value = getattr(self, val_name)
            setattr(self, val_name, current_value + value)
            vals_save("user_files/vals.json", val_name, current_value + value)
        else:
            print(f"Error: Variable '{val_name}' not found.")

    def set(self, val_name, value):
        if hasattr(self, val_name):
            setattr(self, val_name, value)
            vals_save("user_files/vals.json", val_name, value)
        else:
            print(f"Error: Variable '{val_name}' not found.")

    def get(self, val_name):
        if hasattr(self, val_name):
            value = getattr(self, val_name)
        return value
    
    def load(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            for variable_name, value in data.items():
                if hasattr(self, variable_name):
                    setattr(self, variable_name, value)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error loading data from {filename}")

    def show(self):
        for attr, value in vars(self).items():
            print(f"[vals.json] - {attr}: {value}")

ai_status = AllStatus()

# AI name
ai_name = "Himeka"
ai_last = "Shindou"
gui_name = "NekoArt Studio"
ai_full_name = f"{ai_name} {ai_last}"
bot_cls = 0
rt_c = 0

# Image gen
igen_lists = {}
ihq = False
iquality = "standard"
iportrait = False
iscene = False
isize = "1024x1024"

@bot.event
async def on_ready():
    # Load vals
    ai_status.load('user_files/vals.json')
    # Đồng bộ hoá commands
    try:
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ {len(synced)} lệnh.")
    except Exception as e:
        print(e)

    # Emojis load
    emojis_take(bot)

    # Load button
    await load_btt()

    # Time circle
    asyncio.create_task(m_check())
    m_check.start()

    print(f"{ai_name} đã khởi động")

    # Continue chat
    if ai_status.iregen:
        umess = f"Your tablet: You are continuing to draw for {ai_status.last_user}"
        message = await mess_id_send(bot, ai_status.pr_ch_id, umess, ai_status.chat_log)
        asyncio.create_task(img_gen(message, ai_status.img_prompt, iquality, isize))

@bot.event
async def on_message(message):
    if message.author == bot.user or message.content.startswith((".", "<")):
        return
    
    # Phản hồi chat
    if message.content:
        user_name = message.author.nick
        if not user_name:
            user_name = message.author.name
        mess = message.content
        umess = "{}: {}".format(user_name, message.content)
        asyncio.create_task(mess_rep(message, mess, umess, ai_status.chat_log))
    
    return

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
            ai_status.set('img_prompt', prompt)
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
            ai_status.set('img_prompt', prompt)
            await img_gen(message, prompt, quality, size)
            return
        else:
            igen_flw = False
            ai_status.set('igen_flw', igen_flw)
                    
# Image gen dall e 3
async def img_gen(interaction, prompt, quality, size):
    global igen_lists, bot_cls
    igen_flw = ai_status.igen_flw
    img_dprt = ai_status.img_dprt
    iregen = ai_status.iregen

    guild = bot.get_guild(server_id)
    emojis = guild.emojis
    emoji = random.choice(emojis)
    if isinstance(interaction, discord.Interaction):
        user_nick = interaction.user.nick
        if not user_nick:
            user_nick = interaction.user.name
    elif isinstance(interaction, discord.Message):
        user_nick = interaction.author.nick
        if not user_nick:
            user_nick = interaction.author.name
    if ai_status.cds_log:
        print(f"[IMG GENERATE] - {user_nick}")
        print()
    embed = discord.Embed(title=f"{ai_name} đang tạo art cho {user_nick}... {emoji}", description=f"🏷️ {prompt}", color=discord.Color.blue())
    view = View(timeout=None)
    view.add_item(irmv_bt)
    if isinstance(interaction, discord.Interaction):
        await interaction.response.send_message(embed=embed, view=view)
    elif isinstance(interaction, discord.Message):
        await interaction.channel.send(embed=embed, view=view)
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
                bot_cls += 1
                if bot_cls == 2:
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
        embed = discord.Embed(description=f"🏷️ {prompt}", color=discord.Color.blue())
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
        if not igen_flw:
            img_dprt = r_prompt
            vals_save('user_files/vals.json', 'img_dprt', img_dprt)
        await dl_img(img, img_id)
        file_path = f'user_files/gen_imgs/{img_id}.png'
        image_file = discord.File(file_path, filename=f"{img_id}.png")
        embed.set_image(url=f"attachment://{image_file.filename}")
        await message.edit(embed=embed, view=view, attachments=[image_file])
    if img or eimg:
        igen_flw = True
        vals_save('user_files/vals.json', 'igen_flw', igen_flw)
    if eimg:
        await mess_send(message, errar, ai_status.chat_log)
    ai_status.update('bot_mood', 1)
    if error_code:
        if "nối" in error_code or "hem" in error_code or "vậy" in error_code:
            await img_gen(message, ai_status.img_prompt, iquality, isize)
    if bot_cls == 2:
        iregen = True
        pr_ch_id = message.channel.id
        last_user = user_nick
        vals_save('user_files/vals.json', 'iregen', iregen)
        vals_save('user_files/vals.json', 'pr_ch_id', pr_ch_id)
        vals_save('user_files/vals.json', 'last_user', last_user)
        await bot.close()
    iregen = False
    vals_save('user_files/vals.json', 'iregen', iregen)
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
# Image Gen
@bot.tree.command(name="igen", description=f"Tạo art")
async def image_gen(interaction: discord.Interaction, prompt: str = None, hq: bool = ihq, portrait: bool = iportrait, scene: bool = iscene):
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
    ai_status.set('img_prompt', prompt)
    await img_gen(interaction, prompt, quality, size)

@bot.tree.command(name="reconnect", description=f"Kết nối lại với {ai_name}.")
async def renew(interaction: discord.Interaction):
    await interaction.response.send_message(f"{ai_name}'s tablet: *đang thiết lập lại kết nối giữa {gui_name} với {ai_name}*", ephemeral=True)
    await bot.close()

@bot.tree.command(name="timeleap", description=f"Gặp {ai_name} ở timeline khác.")
async def newchat(interaction: discord.Interaction):
    global rt_c
    iuser = interaction.user.name
    if rt_c == 0:
        await interaction.response.send_message(f"{ai_name}'s tablet: Hành động này không thể undo, {iuser} chắc chứ?", ephemeral=True)
        rt_c += 1
    else:
        await interaction.response.send_message(f"*Đã quay ngược thời gian lúc {ai_name} mới tham gia NekoArt Studio... 🕒*")
        await CAc.chat.new_chat(c_token)
        ai_status.set('bot_mood', 50)
        if ai_status.cds_log:
            print(f"[NEW CHAT] - {iuser}")
            print()

@bot.tree.command(name="clogs", description=f"Nhật ký của {ai_name}")
async def cslog(interaction: discord.Interaction, chat: bool = False, command: bool = True, status: bool = False, get: str = None):
    if interaction.user.id == dev_id:
        if get:
            val = ai_status.get(get)
            await interaction.response.send_message(f"{val}", ephemeral=True)
        else:
            ai_status.set('chat_log', chat)
            ai_status.set('cds_log', command)
            ai_status.set('st_log', status)
            await interaction.response.send_message(f"`Chat log: {chat}, Command log: {command}, Status log: {status}.`", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name} mới có thể xem nhật ký của cô ấy.`", ephemeral=True)

@bot.tree.command(name="tablet", description=f"{ai_name} tablet")
async def test_cmd(interaction: discord.Interaction):
    if interaction.user.id == dev_id:
        await interaction.response.send_message(f"Pong~!", ephemeral=True)
    else:
        await interaction.response.send_message(f"`Chỉ {ai_name} mới có thể mở tablet của cô ấy.`", ephemeral=True)

# Button call
async def load_btt():
    irmv_bt.callback = irmv_bt_atv
    rg_bt.callback = rg_bt_atv
    rgs_bt.callback = rgs_bt_atv

async def irmv_bt_atv(interaction):
    await interaction.message.delete()

async def rg_bt_atv(interaction):
    img_prompts = igen_lists.get(interaction.message.id)
    prompt = img_prompts['prompt']
    quality = img_prompts['quality']
    size = img_prompts['size']
    await img_gen(interaction, prompt, quality, size)

async def rgs_bt_atv(interaction):
    img_prompts = igen_lists.get(interaction.message.id)
    prompt = img_prompts['r_prompt']
    quality = img_prompts['quality']
    size = img_prompts['size']
    await img_gen(interaction, prompt, quality, size)

# Circle task
@tasks.loop(seconds=60)
async def m_check():
    global rt_c
    rt_c = 0
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    bot_run()