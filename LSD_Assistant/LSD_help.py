from pyrogram import Client
from pyrogram.types import Message
from texts import LSD_help


async def help(client: Client, message: Message):
    await message.edit(LSD_help)