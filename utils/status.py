import discord, datetime, re, pytz

in_idle = "Chilling ✨"
in_work = "Working 🌸"
in_eat = "Eating... 🍱"
in_sleep = "Sleeping... 💤"
in_sleepy = "Sleepy... 💤"
in_bath = "Bathing... 💦"
in_chat = "💬 Chating with"

idle_status = discord.Status.idle
onl_status = discord.Status.online
dnd_status = discord.Status.dnd
invisible = discord.Status.invisible
streaming = discord.Status.streaming

watching = discord.ActivityType.watching
playing = discord.ActivityType.playing
streaming = discord.ActivityType.streaming
listening = discord.ActivityType.listening
custom = discord.ActivityType.custom
competing = discord.ActivityType.competing

now_atv = discord.Activity(type=watching,name=in_idle)
now_stt = idle_status

async def status_change():
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)
    h = vn_time.hour

    # Midnight
    if 0 <= h <= 6:
        await atv_change(watching, in_sleep)
        await stt_change(invisible)

    # Morning
    elif 7 <= h <= 11:
        await atv_change(competing, in_work)
        await stt_change(dnd_status)
    
    # Noon
    elif 12 <= h <= 13:
        await atv_change(playing, in_eat)
        await stt_change(idle_status)

    # Afternoon
    elif 14 <= h <= 17:
        await atv_change(competing, in_work)
        await stt_change(dnd_status)

    # Night
    elif 18 <= h <= 22:
        await atv_change(streaming, in_idle)
        await stt_change(streaming)
    
    # Sleep
    elif h > 22:
        await atv_change(listening, in_sleepy)
        await stt_change(idle_status)

async def atv_change(type, name):
    from utils.bot import bot, ai_status
    global now_atv
    now_atv = discord.Activity(type=type,name=name)
    await bot.change_presence(activity=now_atv,status=now_stt)
    ai_status.set('ai_stt', name)
    return now_atv

async def stt_change(stt):
    from utils.bot import bot
    global now_stt
    now_stt = stt
    await bot.change_presence(activity=now_atv,status=stt)
    return stt

async def stt_inchat(uname):
    global now_atv
    from utils.bot import bot, ai_status
    name = f"{in_chat} {uname}"
    now_atv = discord.Activity(type=listening,name=name)
    await bot.change_presence(activity=now_atv,status=onl_status)
    ai_status.set('ai_stt', name)