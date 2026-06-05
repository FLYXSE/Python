# withdraw.py
import logging
import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from texts import *
from database import get_or_create_user, update_balance
from utils import ensure_subscribed, check_subscription

logger = logging.getLogger(__name__)

withdraw_router = Router(name="withdraw")

class WithdrawStates(StatesGroup):
    ask_count = State()

@withdraw_router.message(F.text == "💸 Вывод баланса")
async def start_withdraw(message: Message, state: FSMContext, bot):
    channels = getattr(bot, "channels", [])
    if not await ensure_subscribed(message, bot, channels):
        return

    user = message.from_user
    user_data = await get_or_create_user(
        user.id, user.username, user.full_name,
        await check_subscription(bot, user.id, channels)
    )

    if user_data["balance"] < 2500:
        await message.answer(INSUFFICIENT_BALANCE)
        return

    await message.answer(ASK_WITHDRAW_COUNT)
    await state.set_state(WithdrawStates.ask_count)

@withdraw_router.message(WithdrawStates.ask_count)
async def process_withdraw_count(message: Message, state: FSMContext, bot):
    try:
        count = int(message.text.strip())
        if count < 1:
            raise ValueError
    except ValueError:
        await message.answer(INVALID_WITHDRAW_COUNT)
        return

    user = message.from_user
    user_data = await get_or_create_user(
        user.id, user.username, user.full_name,
        await check_subscription(bot, user.id, bot.channels)
    )

    cost = 2500 * count
    if user_data["balance"] < cost:
        await message.answer(
            INSUFFICIENT_FOR_COUNT.format(count=count, cost=cost, balance=user_data["balance"])
        )
        await state.clear()
        return

    success_count = 0
    for _ in range(count):
        try:
            success = await bot.gift_premium_subscription(
                user_id=user.id,
                month_count=6,
                star_count=1500,
                text="С любовью от @MemDice ❤️",
            )
            if success:
                success_count += 1
            else:
                logger.warning(f"gift_premium_subscription вернул False для {user.id}")
                break  # Прерываем при первой неудаче
        except Exception as e:
            logger.error(f"Ошибка подарка Premium: {e}")
            break

    if success_count == 0:
        await message.answer(ERROR_WITHDRAW)
    else:
        deduct = 2500 * success_count
        await update_balance(user.id, -deduct)
        new_balance = user_data["balance"] - deduct

        if success_count == count:
            await asyncio.sleep(1)
            await message.answer(
                SUCCESS_WITHDRAW.format(success_count=success_count, cost=deduct)
            )
        else:
            await message.answer(
                PARTIAL_WITHDRAW.format(
                    success_count=success_count,
                    requested=count,
                    cost=deduct,
                    new_balance=new_balance
                )
            )

    await state.clear()