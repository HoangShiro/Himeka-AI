import asyncio, json, os, random, discord, time, datetime, re
from discord.ext import commands, tasks
from discord.ui import View, button

from user_files.config import *
from utils.ai_api import *
from utils.funcs import *
from utils.buttons import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ai_name = "Himeka"
ai_last = "Shindou"
ai_full_name = f"{ai_name} {ai_last}"

# Image gen
igen_lists = {}
ihq = False
iquality = "standard"
iportrait = False
iscene = False
isize = "1024x1024"

# Vals.json
bot_mood = 50
chat_log = False
cds_log = True
st_log = False
igen_flw = False
img_prompt = "sky"
img_dprt = "sea"
default_values = {
    "bot_mood": 50.0,
    "chat_log": False,
    "cds_log": True,
    "st_log": False,
    "igen_flw": False,
    "img_prompt": "sky",
    "img_dprt": "sea"
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

    # Load button
    await load_btt()
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
        mess = message.content
        umess = "{}: {}".format(user_name, message.content)
        
        async with message.channel.typing():
            answ, ain = await CAI(umess)
            if chat_log:
                print(umess)
                print(f"{ain}: {answ}")
                print()
            await message.reply(answ)
            asyncio.create_task(img_gen_chat(message, mess))
    
    return

# Image gen dall e 3 in chat
async def img_gen_chat(message, result):
    global igen_flw, img_prompt, iquality, isize
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
        if re.search(r'gen|create|tạo|vẽ|draw|chụp', result, re.IGNORECASE) and re.search(r'art|img|pic|ảnh|hình|tấm', result, re.IGNORECASE) and not re.search(r'lại|nữa', result, re.IGNORECASE):
            quality, size = await igen_choice(result)
            iquality = quality
            isize = size
            lang = "en"
            translated = text_translate(result, lang)
            prompt = extract_nouns(translated)
            img_prompt = prompt
            vals_save('user_files/vals.json', 'img_prompt', img_prompt)
            await img_gen(message, prompt, quality, size)
            return
        elif re.search(r'gen|create|tạo|vẽ|draw|chụp', result, re.IGNORECASE) and re.search(r'art|img|pic|ảnh|hình|tấm', result, re.IGNORECASE) and re.search(r'lại|nữa', result, re.IGNORECASE):
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
        elif re.search(r'sửa|fix|chuyển|change|đổi|thay|thêm|add|to|qua|chọn|lấy|choose|take', result, re.IGNORECASE):
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
            img_prompt = prompt
            vals_save('user_files/vals.json', 'img_prompt', img_prompt)
            await img_gen(message, prompt, quality, size)
            return
        else:
            igen_flw = False
                    
# Image gen dall e 3
async def img_gen(interaction, prompt, quality, size):
    global bot_mood, igen_lists, igen_flw, img_dprt
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
    try:
        img, r_prompt = await openai_images(prompt, quality, size)
        view.add_item(rgs_bt)
    except Exception as e:
        if hasattr(e, 'response') and hasattr(e.response, 'json') and 'error' in e.response.json():
            error_message = e.response.json()['error']['message']
            error_code = e.response.json()['error']['code']
            print(f"Error while gen art: {error_code} - {error_message}")
            error_message = error_message[:250]
            if "content_policy_violation" in error_code:
                error_code = "Prompt không an toàn... つ﹏⊂"
            elif "rate_limit_exceeded" in error_code:
                error_code = "Đợi 1 phút nữa nhé... ≧﹏≦"
            elif "billing_hard_limit_reached" in error_code:
                error_code = "Hết cá ròi... 〒▽〒"
        else:
            error_code = e
            if "Connection error" in error_code:
                error_code = "Lỗi kết nối... (ˉ﹃ˉ)"
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
    bot_mood +=1
    return

# Correct prompt and gen art again
async def img_regen(message, quality, size, rq):
    case = f"3[{img_dprt}][{rq}]"
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
async def image_gen(interaction: discord.Interaction, prompt: str = img_prompt, hq: bool = ihq, portrait: bool = iportrait, scene: bool = iscene):
    global img_prompt, ihq, iportrait, iscene
    img_prompt = prompt
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
    vals_save('user_files/vals.json', 'img_prompt', prompt)
    await img_gen(interaction, prompt, quality, size)

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
    asyncio.create_task(img_gen(interaction, prompt, quality, size))

async def rgs_bt_atv(interaction):
    img_prompts = igen_lists.get(interaction.message.id)
    prompt = img_prompts['r_prompt']
    quality = img_prompts['quality']
    size = img_prompts['size']
    asyncio.create_task(img_gen(interaction, prompt, quality, size))

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    bot_run()