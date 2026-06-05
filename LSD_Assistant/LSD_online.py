from pyrogram import Client
from pyrogram.types import Message
from pyrogram.raw.functions.account import UpdateStatus
from texts import *
from emoji import *
import asyncio


online_task = None
online_enabled = False


async def keep_online(client: Client):
    """Фоновая задача для поддержания онлайн статуса"""
    global online_enabled
    while online_enabled:
        try:
            await client.invoke(UpdateStatus(offline=False))
            await asyncio.sleep(55)
        except asyncio.CancelledError:
            break
        except Exception:
            await asyncio.sleep(55)


async def online(client: Client, message: Message):
    global online_task, online_enabled

    if len(message.command) < 2:
        status = "включен" if online_enabled else "выключен"
        await message.edit(LSD_online_status.replace("[]", status))
        return

    arg = message.command[1].lower().strip()

    if arg == "+on":
        if online_enabled:
            await message.edit(LSD_online_already_on)
            return

        online_enabled = True
        online_task = asyncio.create_task(keep_online(client))
        await message.edit(LSD_online_on)

    elif arg == "+off":
        if not online_enabled:
            await message.edit(LSD_online_already_off)
            return

        online_enabled = False
        if online_task:
            online_task.cancel()
            try:
                await online_task
            except asyncio.CancelledError:
                pass
            online_task = None

        await message.edit(LSD_online_off)

    else:
        await message.edit(LSD_online_error)
