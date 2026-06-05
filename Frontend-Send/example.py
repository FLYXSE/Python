import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

# ===================== НАСТРОЙКИ =====================
logging.basicConfig(level=logging.INFO)

TOKEN = "2202914218:AAFggBHUpBVeZukJZFJsr9xbiu9w3Bz6Wug/test"  # ← Замени на свой токен

# Создаём бота с HTML-парсингом по умолчанию
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# ===================== КЛАВИАТУРЫ =====================

# Reply-клавиатура (4 кнопки, как ты просил)
reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="крут")],  # 1-я строка
        [KeyboardButton(text="2 кнопка")],  # 2-я строка
        [KeyboardButton(text="3 кнопка"), KeyboardButton(text="4 кнопка")],  # 3-я строка
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# Inline-клавиатура (4 кнопки с разными типами действий)
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 кнопка (URL)", url="https://google.com")],
        [InlineKeyboardButton(text="2 кнопка (Callback)", callback_data="btn_2")],
        [
            InlineKeyboardButton(text="3 кнопка (Callback)", callback_data="btn_3"),
            InlineKeyboardButton(
                text="4 кнопка (Switch)",
                switch_inline_query_current_chat="пример запроса"
            ),
        ],
    ]
)


# ===================== ХЕНДЛЕРЫ =====================

@dp.message(Command(commands=["start", "help"]))
async def cmd_start_help(message: Message):
    await message.answer(
        "<b>Привет!</b>\n\n"
        "Я пример бота на <b>aiogram 3.x</b>.\n"
        "Снизу — Reply-клавиатура.\n"
        "Сейчас пришлю Inline-клавиатуру."
    )
    # Отправляем Reply-клавиатуру
    await message.answer("Reply клавиатура активна ↓", reply_markup=reply_kb)

    # Отправляем Inline-клавиатуру
    await message.answer("Inline клавиатура:", reply_markup=inline_kb)


# Ответ на callback-кнопки
@dp.callback_query(F.data == "btn_2")
async def callback_btn2(callback: CallbackQuery):
    await callback.answer(
        text="✅ Нажата 2 кнопка (callback_data)",
        show_alert=False
    )
    await callback.message.answer("Ты нажал кнопку 2!")


@dp.callback_query(F.data == "btn_3")
async def callback_btn3(callback: CallbackQuery):
    await callback.answer(
        text="✅ Нажата 3 кнопка (callback_data)",
        show_alert=True
    )
    await callback.message.answer("Ты нажал кнопку 3! (alert)")


# Ответ на текст "крут"
@dp.message(F.text == "крут")
async def handle_krut(message: Message):
    await message.answer("круасан 🥐")


# ===================== ЗАПУСК =====================
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())