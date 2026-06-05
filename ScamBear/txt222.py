import asyncio
import json
import logging
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.enums import ButtonStyle


# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS = os.getenv('CHANNELS').split(',')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database setup
DB_FILE = 'bot.db'


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            games INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            stars_spent INTEGER DEFAULT 0,
            stars_refunded INTEGER DEFAULT 0,
            last_game TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            result TEXT,
            timestamp TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


init_db()


# States
class GameStates(StatesGroup):
    subscribed = State()
    waiting_for_guess = State()
    playing = State()


# Callback data factories
class GuessCallback(CallbackData, prefix="guess"):
    range: str


class CheckSubCallback(CallbackData, prefix="check_sub"):
    pass


class PlayAgainCallback(CallbackData, prefix="play_again"):
    pass


# Helper functions
async def is_subscribed(bot: Bot, user_id: int) -> bool:
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ('member', 'administrator', 'creator'):
                return False
        except Exception as e:
            logging.error(f"Error checking subscription for {channel}: {e}")
            return False
    return True


def get_main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Играть", icon_custom_emoji_id='5400131775047401473')],
        [KeyboardButton(text="Статистика", icon_custom_emoji_id='5402351482865451009')],
        [KeyboardButton(text="О боте", icon_custom_emoji_id='5399911297196228609')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def get_guess_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="1️⃣➖2️⃣", callback_data=GuessCallback(range="1-2").pack()),
        InlineKeyboardButton(text="3️⃣➖4️⃣", callback_data=GuessCallback(range="3-4").pack()),
        InlineKeyboardButton(text="5️⃣➖6️⃣", callback_data=GuessCallback(range="5-6").pack())
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def get_sub_keyboard() -> InlineKeyboardMarkup:
    keyboard = []
    for channel in CHANNELS:
        keyboard.append([InlineKeyboardButton(text=f"Подписаться на {channel}", url=f"https://t.me/{channel[1:]}", icon_custom_emoji_id='5402583681682374657')])
    keyboard.append([InlineKeyboardButton(text="Проверить", callback_data=CheckSubCallback().pack(), icon_custom_emoji_id='5402084434683887617', style='success')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_play_again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Играть ещё раз!", callback_data=PlayAgainCallback().pack(), icon_custom_emoji_id='5400131775047401473')]])


async def update_stats(user_id: int, won: bool):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if won:
        cursor.execute(
            'UPDATE users SET games = games + 1, wins = wins + 1, stars_refunded = stars_refunded + 1 WHERE user_id = ?',
            (user_id,))
    else:
        cursor.execute('UPDATE users SET games = games + 1, stars_spent = stars_spent + 1 WHERE user_id = ?',
                       (user_id,))
    cursor.execute('UPDATE users SET last_game = ? WHERE user_id = ?', (datetime.now(), user_id))
    conn.commit()
    conn.close()


async def log_transaction(user_id: int, amount: int, result: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (user_id, amount, result, timestamp) VALUES (?, ?, ?, ?)',
                   (user_id, amount, result, datetime.now()))
    conn.commit()
    conn.close()


async def get_stats(user_id: int) -> str:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT games, wins, stars_spent, stars_refunded FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        games, wins, spent, refunded = 0, 0, 0, 0
    else:
        games, wins, spent, refunded = row
    percent = (wins / games * 100) if games > 0 else 0
    return f"<tg-emoji emoji-id='5402351482865451009'>📊</tg-emoji> Твоя статистика:\n<tg-emoji emoji-id='5399976108252725249'>🎮</tg-emoji> Игр: {games}\n<tg-emoji emoji-id='5400033892742725633'>👑</tg-emoji> Побед: {wins} ({percent:.1f}%)\n<tg-emoji emoji-id='5402386916345643009'>🗑</tg-emoji> Звёзд сожжено: {spent}\n<tg-emoji emoji-id='5399905580594757633'>⭐️</tg-emoji> Звёзд возвращено: {refunded}"


# Handlers
async def start_handler(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    # Ensure user exists
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

    subscribed = await is_subscribed(bot, user_id)
    if subscribed:
        await state.set_state(GameStates.subscribed)
        await message.answer(
            "<tg-emoji emoji-id='5400220040920301569'>🔥</tg-emoji> Добро пожаловать в MemDice!\n"
            "<tg-emoji emoji-id='5400347129002590209'>⬇️</tg-emoji> Для игры используйте кнопки меню.",
            reply_markup=get_main_menu())
    else:
        await message.answer(
            "<tg-emoji emoji-id='5400220040920301569'>🔥</tg-emoji> Добро пожаловать в MemDice!\n"
            "<tg-emoji emoji-id='5400347129002590209'>⬇️</tg-emoji> Для начала нужно подписаться на каналы.", reply_markup=get_sub_keyboard())


async def check_sub_callback(query: types.CallbackQuery, callback_data: CheckSubCallback, state: FSMContext, bot: Bot):
    user_id = query.from_user.id
    subscribed = await is_subscribed(bot, user_id)
    if subscribed:
        await state.set_state(GameStates.subscribed)
        await query.message.delete()
        await query.message.answer("<tg-emoji emoji-id='5400220040920301569'>🔥</tg-emoji> Добро пожаловать в MemDice!\n"
            "<tg-emoji emoji-id='5400347129002590209'>⬇️</tg-emoji> Для игры используйте кнопки меню.", reply_markup=get_main_menu())
    else:
        await query.answer("Ты ещё не подписан на все каналы. Подпишись и попробуй снова.", show_alert=True)


async def play_handler(message: types.Message, state: FSMContext, bot: Bot):
    subscribed = await is_subscribed(bot, message.from_user.id)
    if not subscribed:
        await message.answer("<tg-emoji emoji-id='5400005258195763201'>🚫</tg-emoji> Подпишись на каналы!", reply_markup=get_sub_keyboard())
        return
    await state.set_state(GameStates.subscribed)  # Ensure state is set
    current_state = await state.get_state()
    if current_state == GameStates.waiting_for_guess or current_state == GameStates.playing:
        await message.answer("Ты уже в процессе игры. Заверши текущую!")
        return
    await state.set_state(GameStates.waiting_for_guess)
    await message.answer("<tg-emoji emoji-id='5400220040920301569'>🔥</tg-emoji> Игра началась!\n<tg-emoji emoji-id='5402626300642852865'>🕯</tg-emoji>Выбери диапазон кубика:",
                         reply_markup=get_guess_keyboard())


async def guess_callback(query: types.CallbackQuery, callback_data: GuessCallback, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != GameStates.waiting_for_guess:
        await query.answer("⚠️ Сначала нажми 'Играть'!")
        return
    user_id = query.from_user.id

    # Check last game time to prevent spam (e.g., < 5 seconds ago)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT last_game FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0]:
        last_time = datetime.fromisoformat(row[0])
        if (datetime.now() - last_time).seconds < 5:
            await query.answer("⚠️ Spam Alert!")
            return

    # Store guess
    await state.update_data(guess=callback_data.range)
    await state.set_state(GameStates.playing)

    # Prepare payload
    payload = json.dumps({"u": user_id, "g": callback_data.range})

    # Send invoice
    await bot.send_invoice(
        chat_id=query.message.chat.id,
        title="🎲 MemDice",
        description="Оплата броска.",
        payload=payload,
        provider_token="",  # Empty for Stars
        currency="XTR",
        prices=[types.LabeledPrice(label="Ставка", amount=1)]
    )
    await query.answer("<tg-emoji emoji-id='5400347129002590209'>⬇️</tg-emoji> Оплатите бросок кубика.")


async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment_handler(message: types.Message, state: FSMContext, bot: Bot):
    payment = message.successful_payment
    payload = json.loads(payment.invoice_payload)
    user_id = payload["u"]
    guess = payload["g"]

    if user_id != message.from_user.id:
        logging.error(f"Payload user_id mismatch: {user_id} vs {message.from_user.id}")
        return

    # Log payment
    await log_transaction(user_id, 1, "payment")

    # Send dice
    dice_message = await bot.send_dice(chat_id=message.chat.id, emoji="🎲")
    await asyncio.sleep(4)
    value = dice_message.dice.value

    # Check win
    low, high = map(int, guess.split("-"))
    won = low <= value <= high

    result_text = f"<tg-emoji emoji-id='5400376901715886081'>💎</tg-emoji> Выпало: {value}\n<tg-emoji emoji-id='5399850136861933569'>✏️</tg-emoji> Ты выбирал: {guess}\n"
    if won:
        result_text += "<tg-emoji emoji-id='5400033892742725633'>👑</tg-emoji> Выигрыш!"
        try:
            await bot.refund_star_payment(user_id=user_id,
                                          telegram_payment_charge_id=payment.telegram_payment_charge_id)
            await log_transaction(user_id, 1, "refund")
        except Exception as e:
            logging.error(f"Refund error: {e}")
            result_text += "\nRefund error: {e}"
    else:
        result_text += "<tg-emoji emoji-id='5400049238660874241'>🌧</tg-emoji> Проигрыш!"

    # Update stats
    await update_stats(user_id, won)

    # Send result
    await message.answer(result_text, reply_markup=get_play_again_keyboard())

    # Reset state
    await state.set_state(GameStates.subscribed)


async def play_again_callback(query: types.CallbackQuery, callback_data: PlayAgainCallback, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)
    await play_handler(query.message, state, query.bot)


async def stats_handler(message: types.Message, state: FSMContext, bot: Bot):
    subscribed = await is_subscribed(bot, message.from_user.id)
    if not subscribed:
        await message.answer("<tg-emoji emoji-id='5400005258195763201'>🚫</tg-emoji> Подпишись на каналы!", reply_markup=get_sub_keyboard())
        return
    await state.set_state(GameStates.subscribed)  # Ensure state is set
    stats = await get_stats(message.from_user.id)
    await message.answer(stats)


async def about_handler(message: types.Message, state: FSMContext, bot: Bot):
    subscribed = await is_subscribed(bot, message.from_user.id)
    if not subscribed:
        await message.answer("<tg-emoji emoji-id='5400005258195763201'>🚫</tg-emoji> Подпишись на каналы!", reply_markup=get_sub_keyboard())
        return
    await state.set_state(GameStates.subscribed)  # Ensure state is set
    await message.answer("<tg-emoji emoji-id='5400220040920301569'>🔥</tg-emoji> MemDice — игровой бот основанный на Dice и Invoice.\n\n"
                         "<tg-emoji emoji-id='5399859907912531969'>➡️</tg-emoji> Попробуй угадать число которое выпадет на кубике.\n\n"
                         "<tg-emoji emoji-id='5400071027029966849'>✨</tg-emoji> Угадал? Получишь звезды обратно!\n"
                         "<tg-emoji emoji-id='5402552955486339073'>💥</tg-emoji> Не угадал? Звезды останутся в боте!")


# Dispatcher setup
async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register handlers
    dp.message.register(start_handler, CommandStart())
    dp.callback_query.register(check_sub_callback, CheckSubCallback.filter())
    dp.message.register(play_handler, lambda m: m.text == "Играть")
    dp.callback_query.register(guess_callback, GuessCallback.filter())
    dp.pre_checkout_query.register(pre_checkout_handler)
    dp.message.register(successful_payment_handler, lambda m: m.successful_payment is not None)
    dp.callback_query.register(play_again_callback, PlayAgainCallback.filter())
    dp.message.register(stats_handler, lambda m: m.text == "Статистика")
    dp.message.register(about_handler, lambda m: m.text == "О боте")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())