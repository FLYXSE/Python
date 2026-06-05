from pyrogram import Client
from pyrogram.types import Message
from texts import LSD_ping
import time


async def ping(client: Client, message: Message):
    start_time = time.time()
    await message.edit(LSD_ping)
    end_time = time.time()
    
    ping_ms = round((end_time - start_time) * 1000)
    
    updated_text = LSD_ping.replace("[]", f"{ping_ms}")
    await message.edit(updated_text)