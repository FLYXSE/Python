from pyrogram import Client
from pyrogram.types import Message
from texts import LSD_start


async def start(client: Client, message: Message):
    await message.edit(LSD_start)