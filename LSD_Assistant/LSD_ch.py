from pyrogram import Client
from pyrogram.types import Message
from texts import *
from emoji import *


async def ch(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit(LSD_ch_error)
        return

    text = " ".join(message.command[1:])
    channel_id = -1002200544214

    try:
        await client.send_message(channel_id, text)
        await message.edit(LSD_ch_success)
    except Exception as e:
        error_text = LSD_ch_error_send.replace("[]", str(e)[:200])
        await message.edit(error_text)
