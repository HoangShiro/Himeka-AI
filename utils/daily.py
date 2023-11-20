import asyncio, json, os, random, discord, time, datetime, re, pytz
from discord.ext import commands, tasks
from discord.ui import View, button
from utils.ai_api import *
from utils.funcs import *

# Circle task
@tasks.loop(seconds=60)
async def m_check():
    from utils.bot import bot, ai_status, ai_name
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)

    # Nhắc tới giờ làm việc
    if ai_status.day_time:
        if vn_time.hour == 8:
            ai_status.set('day_time', False)
            note = f"{ai_name}'s tablet: 8h AM now, you should wake up prepare for work."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await voice_rcn()
                if ai_status.sleeping:
                    ai_status.set('sleeping', False)
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} thức dậy.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")
                await bot.change_presence(activity=discord.Activity(
                                                type=discord.ActivityType.competing,
                                                name="Working 🌸"
                                            ),
                                            status=discord.Status.online)

    # Tới giờ nghỉ trưa
    if ai_status.non_time:
        if vn_time.hour == 12:
            ai_status.set('non_time', False)
            note = f"{ai_name}'s tablet: Non time now (12h AM), you should go to lunch and take a nap."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await v_leave_nc()
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} đi ăn trưa.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")
                await bot.change_presence(activity=discord.Activity(
                                                type=discord.ActivityType.playing,
                                                name="Eating 🍱"
                                            ),
                                            status=discord.Status.idle)

    # Giờ làm việc chiều
    if ai_status.atn_time:
        if vn_time.hour == 14:
            ai_status.set('atn_time', False)
            note = f"{ai_name}'s tablet: 14h PM now, you should go back to work."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await voice_rcn()
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} tiếp tục công việc buổi chiều.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")
                await bot.change_presence(activity=discord.Activity(
                                                type=discord.ActivityType.competing,
                                                name="Working 🌸"
                                            ),
                                            status=discord.Status.online)

    # Tới giờ đi ngủ
    if ai_status.night_time:
        if vn_time.hour == 23:
            ai_status.set('night_time', False)
            note = f"{ai_name}'s tablet: bed time now (23h PM), you should go to sleep."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await v_leave_nc()
                ai_status.set('sleeping', True)
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} đi ngủ.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")

                await bot.change_presence(activity=discord.Activity(
                                                type=discord.ActivityType.watching,
                                                name="Sleeping... 💤"
                                            ),
                                            status=discord.Status.dnd)
    # Reset time
    if not ai_status.day_time:
        if vn_time.hour == 1 or vn_time.hour == 5:
            ai_status.set('day_time', True)
            ai_status.set('non_time', True)
            ai_status.set('atn_time', True)
            ai_status.set('night_time', True)
