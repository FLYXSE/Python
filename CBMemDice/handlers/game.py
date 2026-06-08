import asyncio
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import game_rules_kb, back_to_game_kb, cancel_kb
import database
from utils import log_game, safe_edit
import texts

router = Router()


class GameStates(StatesGroup):
    waiting_bet = State()


@router.callback_query(lambda c: c.data == "play")
async def show_rules(callback: types.CallbackQuery):
    await safe_edit(callback.message, texts.GAME_RULES, reply_markup=game_rules_kb())
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_game")
async def start_game(callback: types.CallbackQuery, state: FSMContext):
    user = database.get_user(callback.from_user.id)
    if not user:
        await callback.answer(texts.USER_NOT_FOUND, show_alert=True)
        return
    if user["balance"] <= 0:
        await safe_edit(callback.message,
            texts.GAME_NO_BALANCE.format(balance=f"{user['balance']:.2f}"),
            reply_markup=cancel_kb(),
        )
        await callback.answer()
        return
    await safe_edit(callback.message,
        texts.GAME_BET_PROMPT.format(balance=f"{user['balance']:.2f}"),
        reply_markup=cancel_kb(),
    )
    await state.set_state(GameStates.waiting_bet)
    await callback.answer()


@router.message(GameStates.waiting_bet, F.text)
async def process_bet(message: types.Message, state: FSMContext):
    raw = message.text.strip().replace(",", ".")
    try:
        bet = float(raw)
    except ValueError:
        await message.answer(texts.INVALID_NUMBER, reply_markup=cancel_kb())
        return
    if bet <= 0:
        await message.answer(texts.GAME_BET_ZERO, reply_markup=cancel_kb())
        return
    user = database.get_user(message.from_user.id)
    if not user or user["balance"] < bet:
        await message.answer(
            texts.GAME_NO_BALANCE_SHORT.format(balance=f"{user['balance']:.2f}"),
            reply_markup=cancel_kb(),
        )
        return
    bet = round(bet, 2)

    database.update_balance(message.from_user.id, -bet)

    dice_msg = await message.answer_dice(emoji="🎲")
    roll = dice_msg.dice.value
    await asyncio.sleep(3)

    multiplier = texts.MULTIPLIERS[roll]
    win_amount = round(bet * multiplier, 2)

    database.update_balance(message.from_user.id, win_amount)
    database.record_game_result(message.from_user.id, bet, roll, multiplier, win_amount)
    log_game(message.from_user.id, bet, roll, multiplier, win_amount)

    current = database.get_user(message.from_user.id)
    balance = current["balance"] if current else 0

    win_prefix = "<tg-emoji emoji-id='5402505173975171073'>🎉</tg-emoji> Выигрыш: +" if win_amount > 0 else "<tg-emoji emoji-id='5402505173975171073'>🎉</tg-emoji> Результат: "
    win_line = f"{win_prefix}<code>{win_amount:.2f}</code> USDT\n"

    await message.answer(
        texts.GAME_RESULT_TEMPLATE.format(
            result_line=texts.ROLL_RESULTS[roll],
            bet=f"{bet:.2f}",
            multiplier=multiplier,
            win_line=win_line,
            balance=f"{balance:.2f}",
        ),
        reply_markup=back_to_game_kb(),
    )
    await state.clear()
