import logging
import os
from typing import Optional
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest


async def safe_edit(message: Message, text: str, reply_markup=None) -> Optional[Message]:
    try:
        return await message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return message
        raise

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "games.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("dice_bot")


def log_game(telegram_id: int, bet: float, roll: int, multiplier: float, win_amount: float):
    logger.info(
        "GAME | user=%d | bet=%.2f | roll=%d | multiplier=%.2f | win=%.2f",
        telegram_id, bet, roll, multiplier, win_amount,
    )


def log_deposit(telegram_id: int, amount: float, invoice_id: str, status: str):
    logger.info(
        "DEPOSIT | user=%d | amount=%.2f | invoice=%s | status=%s",
        telegram_id, amount, invoice_id, status,
    )


def log_withdraw(telegram_id: int, amount: float, target_id: int, status: str):
    logger.info(
        "WITHDRAW | user=%d | amount=%.2f | target=%d | status=%s",
        telegram_id, amount, target_id, status,
    )
