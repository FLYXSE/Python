import aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import asyncio

BOT_TOKEN = "2202914218:AAEcTY9Uui5P786Y6HcdaEfDQgQJmgLAd9g/test"

bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"<tg-emoji emoji-id='5373164573043982337'>✅</tg-emoji> <code>БОРОКИН Я НАПИСАЛ БЕЗ ГПТ!</code>")




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("БОРОКИН Я НАПИСАЛ БЕЗ ГПТ!")
    asyncio.run(main())