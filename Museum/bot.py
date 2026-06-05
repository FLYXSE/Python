# ============================================================
#                         ОГЛАВЛЕНИЕ
# ============================================================
#  1. Импорты и токен
#  2. Клавиатуры
#     2.1 Основная клавиатура
#     2.2 Inline-клавиатуры локаций
#  3. Хендлеры команд
#     3.1 /start
#  4. Хендлеры локаций
#     4.1 Лакацыя №1
#     4.2 Лакацыя №2 + callback'и
#     4.3 Лакацыя №3 + callback'и
#     4.4 Лакацыя №4
#     4.5 Лакацыя №5
#  5. Регистрация хендлеров
#  6. Запуск бота
# ============================================================


# ============================================================
# 1. Импорты и токен
# ============================================================

import os
from aiohttp import web
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile,
)
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import time
from aiogram.enums import ButtonStyle

TOKEN = "8191285007:AAHHQG1HIQgdC0SAHnw4F-9fbgA8kchRzR0"


# ============================================================
# 2. Клавиатуры
# ============================================================

# ------------------------------------------------------------
# 2.1 Основная клавиатура
# ------------------------------------------------------------

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Лакацыя №1", style=ButtonStyle.SUCCESS),
            KeyboardButton(text="Лакацыя №2", style=ButtonStyle.SUCCESS),
        ],
        [
            KeyboardButton(text="Лакацыя №3", style=ButtonStyle.SUCCESS),
            KeyboardButton(text="Лакацыя №4", style=ButtonStyle.SUCCESS),
        ],
        [
            KeyboardButton(text="Лакацыя №5", style=ButtonStyle.SUCCESS)
        ],
    ],
    resize_keyboard=True
)


# ------------------------------------------------------------
# 2.2 Inline-клавиатуры локаций
# ------------------------------------------------------------

# === Для Лакацыя №2 ===
def loca_2_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🪆 Лепельскі строй", callback_data="baby_1")
    kb.button(text="🪆 Расонскі строй", callback_data="baby_2")
    kb.button(text="🪆 Ваўкавыска-Камянецкі строй", callback_data="baby_3")
    kb.button(text="🪆 Навагрудскi строй", callback_data="baby_4")
    kb.button(text="🪆 Пухавіцкі строй", callback_data="baby_5")
    kb.button(text="🪆 Ляхавіцкі строй", callback_data="baby_6")
    kb.button(text="🪆 Магілёўскі строй", callback_data="baby_7")
    kb.button(text="🪆 Неглюбскі строй", callback_data="baby_8")
    kb.button(text="🪆 Маларыцкі строй", callback_data="baby_9")
    kb.button(text="🪆 Мотальскі строй", callback_data="baby_10")
    kb.button(text="🪆 Калінкавіцкі строй", callback_data="baby_11")
    kb.button(text="🪆 Давыд-Гарадоцка-Тураўскі строй", callback_data="baby_12")
    kb.adjust(1)
    return kb.as_markup()


# Кнопка «Назад» для Лакацыя №2
def loca_2_back_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Назад", callback_data="loca2_back", style=ButtonStyle.DANGER)
    kb.adjust(1)
    return kb.as_markup()


# === Для Лакацыя №3 ===
def loca_3_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🪧 Пранік", callback_data="Loca3_1")
    kb.button(text="🪧 Мяліца", callback_data="Loca3_2")
    kb.button(text="🪧 Трапло і Грэбень", callback_data="Loca3_3")
    kb.button(text="🪧 Прасніца", callback_data="Loca3_4")
    kb.button(text="🪧 Верацяно", callback_data="Loca3_01")
    kb.button(text="🪧 Калаўрот", callback_data="Loca3_5")
    kb.button(text="🪧 Сукала", callback_data="Loca3_02")
    kb.button(text="🪧 Кросны і Бёрда", callback_data="Loca3_6")
    kb.button(text="🪧 Чаўнок і Ночва", callback_data="Loca3_7")
    kb.button(text="🪧 Валок і рубель", callback_data="Loca3_8")
    kb.adjust(1)
    return kb.as_markup()


# Кнопка «Назад» для Лакацыя №3
def loca_3_back_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Назад", callback_data="loca3_back", style=ButtonStyle.DANGER)
    kb.adjust(1)
    return kb.as_markup()


# === Для Лакацыя №4 ===
def Loca_5_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Qr #1", url="https://www.google.com/")
    kb.button(text="Qr #2", url="https://www.google.com/")
    kb.button(text="Qr #3", url="https://www.google.com/")
    kb.button(text="Qr #4", url="https://www.google.com/")
    kb.button(text="Qr #5", url="https://www.google.com/")
    kb.button(text="Qr #6", url="https://www.google.com/")
    kb.button(text="Qr #7", url="https://www.google.com/")
    kb.button(text="Qr #8", url="https://www.google.com/")
    kb.button(text="Qr #9", url="https://www.google.com/")
    kb.adjust(3)
    return kb.as_markup()


# ============================================================
# 3. Хендлеры команд
# ============================================================

# ------------------------------------------------------------
# 3.1 /start
# ------------------------------------------------------------

async def start_handler(message: Message):
    voice = FSInputFile("start.m4a")
    
    await message.answer_voice(
        voice=voice,
        caption="👋 Добры дзень!\n🌾 Вас вітае аўдыягід музейнай экспазіцыі “Лёсу палатно”",
        reply_markup=main_kb
    )


# ============================================================
# 4. Хендлеры локаций
# ============================================================

# ------------------------------------------------------------
# 4.1 Лакацыя №1
# ------------------------------------------------------------

async def Loca_1(message: Message):
    voice = FSInputFile("Loca_1.m4a")

    await message.answer_voice(
            voice=voice,
            caption="📍 Лакацыя №1.\n🪧 Гісторыка-этнаграфічныя рэгіёны Беларусі канца ХІХ – пачатку ХХ стст."
        )


# ------------------------------------------------------------
# 4.2 Лакацыя №2 + callback'и
# ------------------------------------------------------------

async def Loca_2(message: Message):
    await message.answer(
        text="📍 Лакацыя №2.\n🪧 Беларускі нацыянальны строй\n⬇️ Абярыце строй",
        reply_markup=loca_2_kb()
    )


async def loca2_back(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="📍 Лакацыя №2.\n🪧 Беларускі нацыянальны строй\n⬇️ Абярыце строй",
        reply_markup=loca_2_kb()
    )
    await call.answer()


async def baby1(call: CallbackQuery):
    voice = FSInputFile("baby_1.m4a")

    await call.answer("🪆 Лепельскі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Лепельскі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby2(call: CallbackQuery):
    voice = FSInputFile("baby_2.m4a")

    await call.answer("🪆 Расонскі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Расонскі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby3(call: CallbackQuery):
    voice = FSInputFile("baby_3.m4a")

    await call.answer("🪆 Ваўкавыска-Камянецкі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Ваўкавыска-Камянецкі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby4(call: CallbackQuery):
    voice = FSInputFile("baby_4.m4a")

    await call.answer("🪆 Навагрудскi строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Навагрудскi строй",
        reply_markup=loca_2_back_kb()
    )


async def baby5(call: CallbackQuery):
    voice = FSInputFile("baby_5.m4a")

    await call.answer("🪆 Пухавіцкі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Пухавіцкі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby6(call: CallbackQuery):
    voice = FSInputFile("baby_6.m4a")

    await call.answer("🪆 Ляхавіцкі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Ляхавіцкі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby7(call: CallbackQuery):
    voice = FSInputFile("baby_7.m4a")

    await call.answer("🪆 Магілёўскі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Магілёўскі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby8(call: CallbackQuery):
    voice = FSInputFile("baby_8.m4a")

    await call.answer("🪆 Неглюбскі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Неглюбскі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby9(call: CallbackQuery):
    voice = FSInputFile("baby_9.m4a")

    await call.answer("🪆 Маларыцкі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Маларыцкі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby10(call: CallbackQuery):
    voice = FSInputFile("baby_10.m4a")

    await call.answer("🪆 Мотальскі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Мотальскі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby11(call: CallbackQuery):
    voice = FSInputFile("baby_11.m4a")

    await call.answer("🪆 Калінкавіцкі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Калінкавіцкі строй",
        reply_markup=loca_2_back_kb()
    )


async def baby12(call: CallbackQuery):
    voice = FSInputFile("baby_12.m4a")

    await call.answer("🪆 Давыд-Гарадоцка-Тураўскі строй", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪆 Давыд-Гарадоцка-Тураўскі строй",
        reply_markup=loca_2_back_kb()
    )



# ------------------------------------------------------------
# 4.3 Лакацыя №3 + callback'и
# ------------------------------------------------------------

async def Loca_3(message: Message):
    await message.answer(
        text="📍 Лакацыя №3.\n🪧 Прадзенне і ткацтва\n⬇️ Абярыце прадмет",
        reply_markup=loca_3_kb()
    )


async def loca3_back(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="📍 Лакацыя №3.\n🪧 Прадзенне і ткацтва\n⬇️ Абярыце прадмет",
        reply_markup=loca_3_kb()
    )
    await call.answer()


async def Loca3_1(call: CallbackQuery):
    voice = FSInputFile("Loca3_1.m4a")

    await call.answer("🪧 Пранік", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Пранік",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_2(call: CallbackQuery):
    voice = FSInputFile("Loca3_2.m4a")

    await call.answer("🪧 Мяліца", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Мяліца (церніцы)",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_3(call: CallbackQuery):
    voice = FSInputFile("Loca3_3.m4a")

    await call.answer("🪧 Трапло і Грэбень", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Трапло (трапачка) і Драўляны грэбень",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_4(call: CallbackQuery):
    voice = FSInputFile("Loca3_4.m4a")

    await call.answer("🪧 Прасніца", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Прасніца",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_01(call: CallbackQuery):
    voice = FSInputFile("Loca_01.m4a")

    await call.answer("🪧 Верацяно", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Верацяно",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_5(call: CallbackQuery):
    voice = FSInputFile("Loca3_5.m4a")

    await call.answer("🪧 Калаўрот", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Калаўрот",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_02(call: CallbackQuery):
    voice = FSInputFile("Loca_02.m4a")

    await call.answer("🪧 Сукала", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Сукала",
        reply_markup=loca_3_back_kb()
    )

async def Loca3_6(call: CallbackQuery):
    voice = FSInputFile("Loca3_6.m4a")

    await call.answer("🪧 Кросны і Бёрда", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Кросны і Бёрда (бярдо)",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_7(call: CallbackQuery):
    voice = FSInputFile("Loca3_7.m4a")

    await call.answer("🪧 Чаўнок і Ночва", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Чаўнок і Ночва (начоўка)",
        reply_markup=loca_3_back_kb()
    )


async def Loca3_8(call: CallbackQuery):
    voice = FSInputFile("Loca3_8.m4a")

    await call.answer("🪧 Валок і рубель", show_alert=False)
    await call.message.delete()
    await call.message.answer_voice(
        voice=voice,
        caption="🪧 Валок (качолка) і рубель",
        reply_markup=loca_3_back_kb()
    )


# ------------------------------------------------------------
# 4.4 Лакацыя №4
# ------------------------------------------------------------

async def Loca_4(message: Message):
    voice = FSInputFile("Kyfar.m4a")

    await message.answer_voice(
            voice=voice,
            caption="📍 Лакацыя №4.\n🪧 Куфар"
        )


# ------------------------------------------------------------
# 4.5 Лакацыя №5
# ------------------------------------------------------------

async def Loca_5(message: Message):
    await message.answer(
        text="📍 Лакацыя №5.\n🪧 Сімволіка беларускага арнаменту\n⬇️ Абярыце Qr",
        reply_markup=Loca_5_kb()
    )

# ============================================================
# 5. Регистрация хендлеров
# ============================================================

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(Loca_1, F.text == "Лакацыя №1")
    dp.message.register(Loca_2, F.text == "Лакацыя №2")
    dp.message.register(Loca_3, F.text == "Лакацыя №3")
    dp.message.register(Loca_4, F.text == "Лакацыя №4")
    dp.message.register(Loca_5, F.text == "Лакацыя №5")

    dp.callback_query.register(baby1, F.data == "baby_1")
    dp.callback_query.register(baby2, F.data == "baby_2")
    dp.callback_query.register(baby3, F.data == "baby_3")
    dp.callback_query.register(baby4, F.data == "baby_4")
    dp.callback_query.register(baby5, F.data == "baby_5")
    dp.callback_query.register(baby6, F.data == "baby_6")
    dp.callback_query.register(baby7, F.data == "baby_7")
    dp.callback_query.register(baby8, F.data == "baby_8")
    dp.callback_query.register(baby9, F.data == "baby_9")
    dp.callback_query.register(baby10, F.data == "baby_10")
    dp.callback_query.register(baby11, F.data == "baby_11")
    dp.callback_query.register(baby12, F.data == "baby_12")
    dp.callback_query.register(loca2_back, F.data == "loca2_back")

    dp.callback_query.register(Loca3_1, F.data == "Loca3_1")
    dp.callback_query.register(Loca3_2, F.data == "Loca3_2")
    dp.callback_query.register(Loca3_3, F.data == "Loca3_3")
    dp.callback_query.register(Loca3_4, F.data == "Loca3_4")
    dp.callback_query.register(Loca3_01, F.data == "Loca3_01")
    dp.callback_query.register(Loca3_5, F.data == "Loca3_5")
    dp.callback_query.register(Loca3_02, F.data == "Loca3_02")
    dp.callback_query.register(Loca3_6, F.data == "Loca3_6")
    dp.callback_query.register(Loca3_7, F.data == "Loca3_7")
    dp.callback_query.register(Loca3_8, F.data == "Loca3_8")
    dp.callback_query.register(loca3_back, F.data == "loca3_back")

    await asyncio.gather(
        dp.start_polling(bot)
    )


# ============================================================
# 6. Запуск бота
# ============================================================

if __name__ == "__main__":
    print("@lesy_polotno_bot запущен.")
    asyncio.run(main())