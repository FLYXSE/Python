import aiogram
import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ButtonStyle
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from pydantic.v1 import InvalidLengthForBrand
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Кошелёк", web_app= WebAppInfo(url="https://app.send.tg/")),
         InlineKeyboardButton(text="Обмен", web_app= WebAppInfo(url="https://app.send.tg/swap"))
        ],
        [InlineKeyboardButton(text="P2P", callback_data="p2p"),
         InlineKeyboardButton(text="Биржа", web_app= WebAppInfo(url="https://app.send.tg/trade"))
        ],
        [InlineKeyboardButton(text="Чеки", callback_data="checks"),
         InlineKeyboardButton(text="Счета", callback_data="invoices")
        ],
        [InlineKeyboardButton(text="Crypto Pay", callback_data="pay"),
         InlineKeyboardButton(text="Розыгрыши", callback_data="giveaways")
        ],
        [InlineKeyboardButton(text="Подписки", callback_data="subscriptions"),
         InlineKeyboardButton(text="Настройки", callback_data="settings")
        ]
        ])


wallet_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Открыть в приложении", web_app= WebAppInfo(url="https://app.send.tg/"))],
        [InlineKeyboardButton(text="Пополнить", web_app= WebAppInfo(url="https://app.send.tg/wallet/deposit")),
         InlineKeyboardButton(text="Вывести", web_app= WebAppInfo(url="https://app.send.tg/wallet/withdraw"))
        ],
        [InlineKeyboardButton(text="Адресная книга", callback_data="address-book")],
        [InlineKeyboardButton(text="Комиссии и лимиты", callback_data="fees-and-limits")]
        ])


p2p_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📈 Купить", callback_data="market-trade-buy"),
         InlineKeyboardButton(text="📉 Продать", callback_data="market-trade-sell")],
        [InlineKeyboardButton(text="🗳 Мои сделки", callback_data="market-manage-orders")],
        [InlineKeyboardButton(text="💸 Создать объявление", callback_data="market-create-offer")],
        [InlineKeyboardButton(text="⚙️ Оплата и валюта", callback_data="market-settings")],
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="open-profile")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back-to-main-menu")]
        ])


checks_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать чек", callback_data="create")],
        [InlineKeyboardButton(text="Создать из чата", callback_data="back-to-main-menu")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back-to-main-menu")]
    ]
)


invoices_kb = 