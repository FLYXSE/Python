import asyncio
import  os
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    PreCheckoutQuery, LabeledPrice, Message, CallbackQuery
from aiogram.enums import ButtonStyle
from pyexpat.errors import messages

BOT_TOKEN = "5001630171:AAE9paypiqK8viMHaTNr4hkEIdQiECzIB3A/test"

bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher(storage=MemoryStorage())

def start_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Valentins Bear", callback_data="valentinsbear", icon_custom_emoji_id="5231197100544360449")],
            [InlineKeyboardButton(text="Valentins Heart", callback_data="valentinsheart", icon_custom_emoji_id="5230956801419116545")],
            [InlineKeyboardButton(text="New Year Bear", callback_data="newyearbear", icon_custom_emoji_id="5233396750865137665")]
        ]
    )

def menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Меню", callback_data="menu", icon_custom_emoji_id="5404400736316424193")]
        ]
    )

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "<tg-emoji emoji-id='5402573738833084417'>🤖</tg-emoji> Добро пожаловать в @LSD_Bear_Bot.\n"
        "<tg-emoji emoji-id='5404550690804596737'>🎁</tg-emoji> Этот бот нужен для отправки <b>временных</b> безлимитных подарков.\n\n\n"
        "<blockquote><tg-emoji emoji-id='5404478458044612609'>❓</tg-emoji> Как вы отправляете подарки если они больше не доступны?\n"
        "<tg-emoji emoji-id='5404327494239125505'>💬</tg-emoji> Мы используем новейшие эксплоиты для обхода этого ограничения.</blockquote>",
        reply_markup=start_kb()
    )

@dp.callback_query(F.data == "menu")
async def menu(callback_query: CallbackQuery):
    await callback_query.message.answer(
        "<tg-emoji emoji-id='5402573738833084417'>🤖</tg-emoji> Добро пожаловать в @LSD_Bear_Bot.\n"
        "<tg-emoji emoji-id='5404550690804596737'>🎁</tg-emoji> Этот бот нужен для отправки <b>временных</b> безлимитных подарков.\n\n\n"
        "<blockquote><tg-emoji emoji-id='5404478458044612609'>❓</tg-emoji> Как вы отправляете подарки если они больше не доступны?\n"
        "<tg-emoji emoji-id='5404327494239125505'>💬</tg-emoji> Мы используем новейшие эксплоиты для обхода этого ограничения.</blockquote>",
        reply_markup=start_kb()
    )


@dp.callback_query(F.data == "valentinsbear")
async def valentinsbear(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    payload = f"valentinsbear:{user_id}"
    await callback_query.message.answer_invoice(
        title="🧸 Valentins Bear",
        description="Подарок от @LSD_Bear_Bot",
        prices=[LabeledPrice(label="Valentins Bear", amount=60)],
        payload=payload,
        currency="XTR",
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    # Можно проверить, что payload соответствует нашим товарам
    if query.invoice_payload.startswith(("valentinsbear", "valentinsheart", "newyearbear")):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Неизвестный товар")


@dp.callback_query(F.data == "valentinsheart")
async def valentinsheart(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    payload = f"valentinsheart:{user_id}"
    await callback_query.message.answer_invoice(
        title="💖 Valentins Heart",
        description="Подарок от @LSD_Bear_Bot",
        prices=[LabeledPrice(label="Valentins Heart", amount=25)],
        payload=payload,
        currency="XTR",
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    # Можно проверить, что payload соответствует нашим товарам
    if query.invoice_payload.startswith(("valentinsbear", "valentinsheart", "newyearbear")):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Неизвестный товар")


@dp.callback_query(F.data == "newyearbear")
async def newyearbear(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    payload = f"newyearbear:{user_id}"
    await callback_query.message.answer_invoice(
        title="☃️ New Year Bear",
        description="Подарок от @LSD_Bear_Bot",
        prices=[LabeledPrice(label="New Year Bear", amount=60)],
        payload=payload,
        currency="XTR",
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    # Можно проверить, что payload соответствует нашим товарам
    if query.invoice_payload.startswith(("valentinsbear", "valentinsheart", "newyearbear")):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Неизвестный товар")



@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    # Разделяем payload на товар и user_id
    if ":" in payload:
        item, user_id_str = payload.split(":", 1)
        user_id = int(user_id_str)
    else:
        # Если формат другой — обрабатываем как раньше
        item = payload
        user_id = message.from_user.id

    # Проверяем, что user_id совпадает с тем, кто оплатил (для безопасности)
    if user_id != message.from_user.id:
        # Возможна подмена? Вряд ли, но лучше проверить
        await message.answer("Ошибка: несоответствие пользователя")
        return

    # Выбираем ответ в зависимости от товара
    if item == "valentinsbear":
        text = ("<tg-emoji emoji-id='5404797810337906689'>⚠️</tg-emoji> Произошла ошибка.\n\n"
                "<tg-emoji emoji-id='5404550690804596737'>🎁</tg-emoji> Невозможно отправить подарок <tg-emoji emoji-id='5231197100544360449'>🧸</tg-emoji> Valentins Bear.\n\n"
                "<tg-emoji emoji-id='5402409366139699201'>🕓</tg-emoji> Попробуйте через 5 минут.")
    elif item == "valentinsheart":
        text = ("<tg-emoji emoji-id='5404797810337906689'>⚠️</tg-emoji> Произошла ошибка.\n\n"
        "<tg-emoji emoji-id='5404550690804596737'>🎁</tg-emoji> Невозможно отправить подарок <tg-emoji emoji-id='5230956801419116545'>💖</tg-emoji> Valentins Heart.\n\n"
        "<tg-emoji emoji-id='5402409366139699201'>🕓</tg-emoji> Попробуйте через 5 минут.")
    elif item == "newyearbear":
        text = ("<tg-emoji emoji-id='5404797810337906689'>⚠️</tg-emoji> Произошла ошибка.\n\n"
        "<tg-emoji emoji-id='5404550690804596737'>🎁</tg-emoji> Невозможно отправить подарок <tg-emoji emoji-id='5233396750865137665'>☃️</tg-emoji> New Year Bear.\n\n"
        "<tg-emoji emoji-id='5402409366139699201'>🕓</tg-emoji> Попробуйте через 5 минут.")
    else:
        text = "Неизвестный товар"

    await message.answer(text, reply_markup=menu_kb())



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("ScamBear Запущен!")
    asyncio.run(main())