import asyncio, json, os, random, discord, time, datetime, re, pytz
from discord.ext import commands, tasks
from discord.ui import View, button
from utils.ai_api import *
from utils.funcs import *
from utils.status import *


# Circle task
@tasks.loop(seconds=1800)
async def h_check():
    from utils.bot import ai_status, ai_name
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)

    # Nhắc tới giờ làm việc
    if ai_status.day_time:
        if vn_time.hour == 7:
            if ai_status.sleeping:
                await ai_status.set('sleeping', False)
            await ai_status.set('day_time', False)
            note = f"{ai_name}'s tablet: 8h AM now, you should wake up prepare for work."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await voice_rcn()
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} thức dậy.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")

    # Tới giờ nghỉ trưa
    if ai_status.non_time:
        if vn_time.hour == 12:
            await ai_status.set('non_time', False)
            note = f"{ai_name}'s tablet: Noon time now (12h AM), you should go to lunch and take a nap."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await v_leave_nc()
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} đi ăn trưa.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")

    # Giờ làm việc chiều
    if ai_status.atn_time:
        if vn_time.hour == 14:
            await ai_status.set('atn_time', False)
            note = f"{ai_name}'s tablet: 14h PM now, you should go back to work."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await voice_rcn()
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} tiếp tục công việc buổi chiều.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")

    # Tới giờ đi ngủ
    if ai_status.night_time:
        if vn_time.hour == 23:
            await ai_status.set('night_time', False)
            note = f"{ai_name}'s tablet: bed time now (23h PM), you should go to sleep."
            answ = await CAI(note)
            ready = await check_cai_ready(answ)
            if ready:
                await v_leave_nc()
                await ai_status.set('sleeping', True)
                if ai_status.st_log:
                    print(f"{ai_name}'s tablet: đã nhắc {ai_name} đi ngủ.")
                if ai_status.chat_log:
                    print(f"{ai_name}: {answ}")

    # Reset time
    if vn_time.hour == 1 or vn_time.hour == 5:
        if not ai_status.sleeping:
            await ai_status.set('sleeping', True)
        if not ai_status.day_time:
            await ai_status.set('day_time', True)
            await ai_status.set('non_time', True)
            await ai_status.set('atn_time', True)
            await ai_status.set('night_time', True)

@tasks.loop(seconds=random.randint(120, 180))
async def m_check():
    from utils.bot import ai_status
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)
    await status_change()

    # Add money
    if not ai_status.sleeping:
        await money_with_hime()

    if ai_status.sleep_cd > 0:
        await ai_status.update('sleep_cd', -1)
    elif ai_status.sleep_cd == 0:
        if vn_time.hour < 7:
            await ai_status.set('sleeping', True)
        await ai_status.set('sleep_cd', -1)
        await ai_status.set('sleep_rd', False)
        await v_leave_nc()