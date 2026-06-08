import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT DEFAULT '',
            balance REAL DEFAULT 0.0,
            total_games INTEGER DEFAULT 0,
            total_wins INTEGER DEFAULT 0,
            cryptopay_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bet REAL NOT NULL,
            roll INTEGER NOT NULL,
            multiplier REAL NOT NULL,
            win_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('deposit','withdraw','game')),
            amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','completed','failed')),
            invoice_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def get_or_create_user(telegram_id: int, username: str = "") -> sqlite3.Row:
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()
    if user is None:
        conn.execute(
            "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
            (telegram_id, username),
        )
        conn.commit()
        user = conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
    elif username and user["username"] != username:
        conn.execute(
            "UPDATE users SET username = ? WHERE telegram_id = ?",
            (username, telegram_id),
        )
        conn.commit()
        user = conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
    conn.close()
    return user


def get_user(telegram_id: int):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()
    conn.close()
    return user


def update_balance(telegram_id: int, amount: float):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET balance = balance + ? WHERE telegram_id = ?",
        (amount, telegram_id),
    )
    conn.commit()
    conn.close()


def set_balance(telegram_id: int, amount: float):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET balance = ? WHERE telegram_id = ?",
        (amount, telegram_id),
    )
    conn.commit()
    conn.close()


def record_game(telegram_id: int, bet: float, roll: int, multiplier: float, win_amount: float):
    conn = get_connection()
    user = conn.execute(
        "SELECT id FROM users WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()
    if user:
        conn.execute(
            "INSERT INTO games (user_id, bet, roll, multiplier, win_amount) VALUES (?, ?, ?, ?, ?)",
            (user["id"], bet, roll, multiplier, win_amount),
        )
        conn.execute(
            "UPDATE users SET total_games = total_games + 1, total_wins = total_wins + ?, balance = balance + ?, balance = MAX(balance, 0) WHERE telegram_id = ?",
            (1 if win_amount > 0 else 0, win_amount - bet, telegram_id),
        )
        conn.commit()
    conn.close()


def record_game_result(telegram_id: int, bet: float, roll: int, multiplier: float, win_amount: float):
    conn = get_connection()
    user = conn.execute(
        "SELECT id FROM users WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()
    if user:
        conn.execute(
            "INSERT INTO games (user_id, bet, roll, multiplier, win_amount) VALUES (?, ?, ?, ?, ?)",
            (user["id"], bet, roll, multiplier, win_amount),
        )
        conn.execute(
            "UPDATE users SET total_games = total_games + 1, total_wins = total_wins + ? WHERE telegram_id = ?",
            (1 if win_amount > 0 else 0, telegram_id),
        )
        conn.commit()
    conn.close()


def create_transaction(telegram_id: int, tx_type: str, amount: float, status: str = "pending", invoice_id: str = None):
    conn = get_connection()
    user = conn.execute(
        "SELECT id FROM users WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()
    if user:
        conn.execute(
            "INSERT INTO transactions (user_id, type, amount, status, invoice_id) VALUES (?, ?, ?, ?, ?)",
            (user["id"], tx_type, amount, status, invoice_id),
        )
        conn.commit()
        tx_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return tx_id
    conn.close()
    return None


def update_transaction_status(tx_id: int, status: str):
    conn = get_connection()
    conn.execute(
        "UPDATE transactions SET status = ? WHERE id = ?", (status, tx_id)
    )
    conn.commit()
    conn.close()


def get_pending_deposits() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT t.*, u.telegram_id FROM transactions t JOIN users u ON t.user_id = u.id WHERE t.type = 'deposit' AND t.status = 'pending' AND t.invoice_id IS NOT NULL"
    ).fetchall()
    conn.close()
    return rows


def update_transaction_invoice(tx_id: int, invoice_id: str):
    conn = get_connection()
    conn.execute(
        "UPDATE transactions SET invoice_id = ? WHERE id = ?", (invoice_id, tx_id)
    )
    conn.commit()
    conn.close()


def save_cryptopay_id(telegram_id: int, cryptopay_id: int):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET cryptopay_id = ? WHERE telegram_id = ?",
        (cryptopay_id, telegram_id),
    )
    conn.commit()
    conn.close()


def complete_deposit(tx_id: int, telegram_id: int, amount: float):
    conn = get_connection()
    conn.execute(
        "UPDATE transactions SET status = 'completed' WHERE id = ?", (tx_id,)
    )
    conn.execute(
        "UPDATE users SET balance = balance + ? WHERE telegram_id = ?",
        (amount, telegram_id),
    )
    conn.commit()
    conn.close()
