# memdice_bot/database.py
import aiosqlite
from typing import Optional, Dict

DB_NAME = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                balance INTEGER DEFAULT 0,
                total_games INTEGER DEFAULT 0,
                is_subscribed BOOLEAN DEFAULT FALSE
            )
            """
        )
        await db.commit()


async def get_or_create_user(
    user_id: int, username: Optional[str], full_name: str, is_subscribed: bool
) -> Dict:
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (user_id, username, full_name, is_subscribed)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, username, full_name, is_subscribed),
        )
        await db.commit()

        cursor = await db.execute(
            "SELECT user_id, username, full_name, balance, total_games, is_subscribed FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        return {
            "user_id": row[0],
            "username": row[1],
            "full_name": row[2],
            "balance": row[3],
            "total_games": row[4],
            "is_subscribed": bool(row[5]),
        }


async def update_user_info(user_id: int, username: Optional[str], full_name: str, is_subscribed: bool):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users SET username = ?, full_name = ?, is_subscribed = ? WHERE user_id = ?
            """,
            (username, full_name, is_subscribed, user_id),
        )
        await db.commit()


async def add_balance(user_id: int, amount: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id),
        )
        await db.commit()


async def increment_games(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET total_games = total_games + 1 WHERE user_id = ?",
            (user_id,),
        )
        await db.commit()


async def update_balance(user_id: int, delta: int):
    """
    Изменяет баланс на delta (может быть отрицательным для списания).
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (delta, user_id),
        )
        await db.commit()