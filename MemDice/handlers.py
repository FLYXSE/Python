# memdice_bot/handlers.py
import asyncio
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from texts import *
from keyboards import get_main_keyboard, get_subscribe_keyboard
from database import get_or_create_user, update_user_info, add_balance, increment_games
from utils import check_subscription, ensure_subscribed

router = Router()


class GameStates(StatesGroup):
    waiting_payment = State()
    rolling = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user = message.from_user
    username = user.username
    full_name = user.full_name
    channels = getattr(bot, "channels", [])
    texts = globals()

    is_sub = await check_subscription(bot, user.id, channels)
    await update_user_info(user.id, username, full_name, is_sub)
    user_data = await get_or_create_user(user.id, username, full_name, is_sub)

    if not is_sub:
        kb = get_subscribe_keyboard(channels)
        await message.answer(SUBSCRIBE_PROMPT, reply_markup=kb)
    else:
        await message.answer(WELCOME, reply_markup=get_main_keyboard())
        await state.clear()


@router.message(F.text == "🎲 Бросить кубик")
async def start_roll(message: Message, state: FSMContext, bot: Bot):
    if await state.get_state() is not None:
        await message.answer(GAME_IN_PROGRESS)
        return

    channels = getattr(bot, "channels", [])
    if not await ensure_subscribed(message, bot, channels):
        return

    invoice_msg = await message.answer_invoice(
        title="🎲 MemDice",
        description="Счет на оплату броска.",
        prices=[LabeledPrice(label="Один бросок", amount=3000)],
        payload="dice_roll",
        currency="XTR",
    )
    await state.update_data(invoice_msg_id=invoice_msg.message_id)
    await state.set_state(GameStates.waiting_payment)


@router.pre_checkout_query(F.invoice_payload == "dice_roll")
async def pre_checkout_handler(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != GameStates.waiting_payment.state:
        return

    await state.set_state(GameStates.rolling)

    dice_msg = await message.answer_dice(emoji="🎲")
    n = dice_msg.dice.value
    win = n * 1000

    await asyncio.sleep(4)

    username = message.from_user.username or message.from_user.first_name
    result_text = GAME_RESULT.format(username=username, n=n, win=win)
    await message.answer(result_text, reply_to_message_id=dice_msg.message_id)

    user_id = message.from_user.id
    await add_balance(user_id, win)
    await increment_games(user_id)

    data = await state.get_data()
    invoice_msg_id = data.get("invoice_msg_id")

    if invoice_msg_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=invoice_msg_id
            )
            print(f"Инвойс {invoice_msg_id} удалён для пользователя {user_id}")
        except Exception as e:
            print(f"Не удалось удалить инвойс {invoice_msg_id}: {e}")
    
    await state.clear()


@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message, bot: Bot):
    channels = getattr(bot, "channels", [])
    if not await ensure_subscribed(message, bot, channels):
        return

    user_data = await get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
        await check_subscription(bot, message.from_user.id, channels),
    )
    text = PROFILE_TEMPLATE.format(
        username=user_data["username"] or "no_username",
        balance=user_data["balance"],
        games=user_data["total_games"],
    )
    await message.answer(text)


@router.message(F.text == "🤖 О боте")
async def show_about(message: Message, bot: Bot):
    channels = getattr(bot, "channels", [])
    if not await ensure_subscribed(message, bot, channels):
        return
    await message.answer(ABOUT)


# Игнорируем другие сообщения (или можно добавить help)
@router.message()
async def unknown(message: Message):
    await message.answer(f"<tg-emoji emoji-id='5197454136659935233'>✉️</tg-emoji> Я вас не понимаю :(\nИспользуйте кнопки меню <tg-emoji emoji-id='5195136499292569601'>👇</tg-emoji>", reply_markup=get_main_keyboard())