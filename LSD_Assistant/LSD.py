from pyrogram import Client, filters
from pyrogram.types import Message
import logging
import asyncio
import os
from dotenv import load_dotenv
from pyromod import listen

from texts import *
from emoji import *

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

app = Client(
    "LSD_Assistant",
    api_id=api_id,
    api_hash=api_hash,
    test_mode=True
)

# Импорт модулей
from LSD_start import start
from LSD_help import help
from LSD_ping import ping
from LSD_wiki import wiki
from LSD_rand import rand
from LSD_clear import clear
from LSD_ch import ch
#from LSD_info import info
from LSD_online import online
from LSD_mute import mute, check_muted_message

# ====================== ХЕНДЛЕРЫ ======================

@app.on_message(filters.command("start", prefixes="LSD.") & filters.me)
async def start_handler(client: Client, message: Message):
    await start(client, message)


@app.on_message(filters.command("help", prefixes="LSD.") & filters.me)
async def help_handler(client: Client, message: Message):
    await help(client, message)


@app.on_message(filters.command("ping", prefixes="LSD.") & filters.me)
async def ping_handler(client: Client, message: Message):
    await ping(client, message)


@app.on_message(filters.command("wiki", prefixes="LSD.") & filters.me)
async def wiki_handler(client: Client, message: Message):
    await wiki(client, message)


@app.on_message(filters.command("rand", prefixes="LSD.") & filters.me)
async def rand_handler(client: Client, message: Message):
    await rand(client, message)


@app.on_message(filters.command("clear", prefixes="LSD.") & filters.me)
async def clear_handler(client: Client, message: Message):
    await clear(client, message)


@app.on_message(filters.command("ch", prefixes="LSD.") & filters.me)
async def ch_handler(client: Client, message: Message):
    await ch(client, message)


@app.on_message(filters.command("info", prefixes="LSD.") & filters.me)
async def info_handler(client: Client, message: Message):
    await info(client, message)


@app.on_message(filters.command("mute", prefixes="LSD.") & filters.me)
async def mute_handler(client: Client, message: Message):
    await mute(client, message)


@app.on_message(filters.command("online", prefixes="LSD.") & filters.me)
async def online_handler(client: Client, message: Message):
    await online(client, message)


# Хендлер для автоудаления сообщений от замученных пользователей
@app.on_message(filters.private & ~filters.me)
async def muted_check_handler(client: Client, message: Message):
    await check_muted_message(client, message)


# ====================== ЗАПУСК ======================

if __name__ == "__main__":
    print(f"{star} LSD Assistant успешно запущен!")
    app.run()