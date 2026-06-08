from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import profile_kb, deposit_kb, cancel_kb
import database
from services import cryptopay
from utils import log_deposit, log_withdraw, safe_edit
import texts

router = Router()


class DepositStates(StatesGroup):
    waiting_amount = State()


class WithdrawStates(StatesGroup):
    waiting_amount = State()
    waiting_cryptopay_id = State()


@router.callback_query(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    user = database.get_user(callback.from_user.id)
    if not user:
        await callback.answer(texts.USER_NOT_FOUND, show_alert=True)
        return
    ratio = 0.0
    if user["total_games"] > 0:
        ratio = round(user["total_wins"] / user["total_games"], 2)
    text = texts.PROFILE_TEXT.format(
        balance=f"{user['balance']:.2f}",
        total_games=user["total_games"],
        total_wins=user["total_wins"],
        ratio=ratio,
    )
    await safe_edit(callback.message, text, reply_markup=profile_kb())
    await callback.answer()


@router.callback_query(lambda c: c.data == "deposit")
async def deposit_start(callback: types.CallbackQuery, state: FSMContext):
    await safe_edit(callback.message, texts.DEPOSIT_PROMPT, reply_markup=cancel_kb())
    await state.set_state(DepositStates.waiting_amount)
    await callback.answer()


@router.message(DepositStates.waiting_amount, F.text)
async def deposit_amount(message: types.Message, state: FSMContext):
    raw = message.text.strip().replace(",", ".")
    try:
        amount = float(raw)
    except ValueError:
        await message.answer(texts.INVALID_NUMBER, reply_markup=cancel_kb())
        return
    if amount < 1:
        await message.answer(texts.MIN_DEPOSIT, reply_markup=cancel_kb())
        return
    amount = round(amount, 2)

    tx_id = database.create_transaction(message.from_user.id, "deposit", amount, "pending")
    if tx_id is None:
        await message.answer(texts.TX_ERROR, reply_markup=cancel_kb())
        await state.clear()
        return

    payload = f"dep_{message.from_user.id}_{tx_id}"
    invoice = await cryptopay.create_invoice(amount, payload)
    if not invoice or not invoice.get("link"):
        database.update_transaction_status(tx_id, "failed")
        await message.answer(texts.INVOICE_ERROR, reply_markup=cancel_kb())
        await state.clear()
        return

    invoice_id = invoice.get("invoice_id", "")
    link = invoice["link"]

    database.update_transaction_invoice(tx_id, invoice_id)
    log_deposit(message.from_user.id, amount, invoice_id, "created")

    await message.answer(
        texts.INVOICE_CREATED.format(amount=f"{amount:.2f}", link=link),
        reply_markup=deposit_kb(),
    )
    await state.clear()


@router.message(Command("setid"))
async def cmd_setid(message: types.Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        await message.answer(texts.SETID_USAGE, reply_markup=cancel_kb())
        return
    cryptopay_id = int(args[1])
    database.save_cryptopay_id(message.from_user.id, cryptopay_id)
    await message.answer(texts.SETID_DONE.format(cryptopay_id=cryptopay_id))
    await state.clear()


@router.callback_query(lambda c: c.data == "withdraw")
async def withdraw_start(callback: types.CallbackQuery, state: FSMContext):
    user = database.get_user(callback.from_user.id)
    if not user:
        await callback.answer(texts.USER_NOT_FOUND, show_alert=True)
        return
    if not user["cryptopay_id"]:
        await safe_edit(callback.message, texts.WITHDRAW_ASK_ID, reply_markup=cancel_kb())
        await state.set_state(WithdrawStates.waiting_cryptopay_id)
        await callback.answer()
        return
    if user["balance"] < 15:
        await safe_edit(callback.message,
            texts.WITHDRAW_INSUFFICIENT.format(balance=f"{user['balance']:.2f}"),
            reply_markup=profile_kb(),
        )
        await callback.answer()
        return
    await safe_edit(callback.message,
        texts.WITHDRAW_PROMPT.format(balance=f"{user['balance']:.2f}"),
        reply_markup=cancel_kb(),
    )
    await state.set_state(WithdrawStates.waiting_amount)
    await callback.answer()


@router.message(WithdrawStates.waiting_cryptopay_id, F.text)
async def withdraw_set_id(message: types.Message, state: FSMContext):
    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer(texts.INVALID_TARGET_ID, reply_markup=cancel_kb())
        return
    cryptopay_id = int(raw)
    database.save_cryptopay_id(message.from_user.id, cryptopay_id)
    await message.answer(texts.SETID_DONE.format(cryptopay_id=cryptopay_id))

    user = database.get_user(message.from_user.id)
    if user["balance"] < 15:
        await message.answer(
            texts.WITHDRAW_INSUFFICIENT.format(balance=f"{user['balance']:.2f}"),
            reply_markup=profile_kb(),
        )
        await state.clear()
        return
    await message.answer(
        texts.WITHDRAW_PROMPT.format(balance=f"{user['balance']:.2f}"),
        reply_markup=cancel_kb(),
    )
    await state.set_state(WithdrawStates.waiting_amount)


@router.message(WithdrawStates.waiting_amount, F.text)
async def withdraw_amount(message: types.Message, state: FSMContext):
    raw = message.text.strip().replace(",", ".")
    try:
        amount = float(raw)
    except ValueError:
        await message.answer(texts.INVALID_NUMBER, reply_markup=cancel_kb())
        return
    if amount < 15:
        await message.answer(texts.WITHDRAW_MIN, reply_markup=cancel_kb())
        return
    user = database.get_user(message.from_user.id)
    if not user or user["balance"] < amount:
        await message.answer(
            texts.WITHDRAW_NO_FUNDS.format(balance=f"{user['balance']:.2f}"),
            reply_markup=cancel_kb(),
        )
        return
    amount = round(amount, 2)
    target_id = user["cryptopay_id"]

    result = await cryptopay.transfer(int(target_id), amount)
    if result is None:
        await message.answer(texts.WITHDRAW_ERROR, reply_markup=cancel_kb())
        await state.clear()
        return

    new_balance = round(user["balance"] - amount, 2)
    database.set_balance(message.from_user.id, new_balance)
    database.create_transaction(message.from_user.id, "withdraw", amount, "completed")
    log_withdraw(message.from_user.id, amount, int(target_id), "completed")

    await message.answer(
        texts.WITHDRAW_SUCCESS.format(
            amount=f"{amount:.2f}",
            new_balance=f"{new_balance:.2f}",
        ),
        reply_markup=profile_kb(),
    )
    await state.clear()


@router.callback_query(lambda c: c.data == "deposit_back")
async def deposit_back(callback: types.CallbackQuery):
    user = database.get_user(callback.from_user.id)
    ratio = 0.0
    if user and user["total_games"] > 0:
        ratio = round(user["total_wins"] / user["total_games"], 2)
    text = texts.PROFILE_TEXT.format(
        balance=f"{user['balance']:.2f}",
        total_games=user["total_games"],
        total_wins=user["total_wins"],
        ratio=ratio,
    )
    await safe_edit(callback.message, text, reply_markup=profile_kb())
    await callback.answer()
