import asyncio
import logging

import aiogram
from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ButtonStyle
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    LinkPreviewOptions,
    WebAppInfo,
)

from txt import *
from kbs import *

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "7950700639:AAGKbp3aqOLe1Nv-g-tqWZ98VAtR83Mdl_4"

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(start_txt,
                         link_preview_options=LinkPreviewOptions(is_disabled=True),
                         reply_markup=start_kb)


#@dp.callback_query(F.data == "wallet")
#async def wallet(callback: CallbackQuery):
#    await callback.message.edit_text(wallet_txt, link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=wallet_kb)


@dp.callback_query(F.data == "p2p")
async def p2p(callback: CallbackQuery):
    await callback.message.edit_text(p2p_txt,
                                     link_preview_options=LinkPreviewOptions(is_disabled=True),
                                     reply_markup=p2p_kb)


@dp.callback_query(F.data == "back-to-main-menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(start_txt,
                         link_preview_options=LinkPreviewOptions(is_disabled=True),
                         reply_markup=start_kb)
    

@dp.callback_query(F.data == "checks")
async def checks(callback: CallbackQuery):
    await callback.message.edit_text(checks_txt,
                                     link_preview_options=LinkPreviewOptions(is_disabled=True),
                                     reply_markup=checks_kb)
    

@dp.callback_query(F.data == "invoices")
async def invoices(callback: CallbackQuery):
    await callback.message.edit_text(invoices_txt,
                                     link_preview_options=LinkPreviewOptions(is_disabled=True),
                                     reply_markup=invoices_kb)





















async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())