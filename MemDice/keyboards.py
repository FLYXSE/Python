# memdice_bot/keyboards.py
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🎲 Бросить кубик"),
        KeyboardButton(text="💸 Вывод баланса"),
    )
    builder.row(
        KeyboardButton(text="👤 Профиль"),
        KeyboardButton(text="🤖 О боте"),
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def get_subscribe_keyboard(channels: list):
    builder = InlineKeyboardBuilder()
    for channel in channels:
        if channel.startswith("@"):
            uname = channel[1:]
            builder.button(
                text=f"🔗 Подписаться на @{uname}",
                url=f"https://t.me/{uname}",
            )
    builder.adjust(1)
    return builder.as_markup()