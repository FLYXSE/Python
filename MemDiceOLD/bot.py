import asyncio
import json
import os
import time
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from aiogram.client.session.aiohttp import AiohttpSession

import texts
import keyboard

# ───── CONFIG ─────
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DB_FILE = "db.json"
ANTISPAM_SECONDS = 4


bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# ───── DB ─────
def load_db():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


# ───── UTILS ─────
def is_admin(uid: int) -> bool:
    return uid == ADMIN_ID


def is_banned(uid: int) -> bool:
    db = load_db()
    return uid in db["banned"]


def antispam(user_id: int) -> bool:
    db = load_db()
    now = time.time()
    last = db["last_action"].get(str(user_id), 0)

    if now - last < ANTISPAM_SECONDS:
        return False

    db["last_action"][str(user_id)] = now
    save_db(db)
    return True


# ───── /start (PRIVATE ONLY) ─────
@dp.message(F.text.startswith("/start"))
async def start_cmd(message: Message):
    if message.chat.type != "private":
        return

    if is_banned(message.from_user.id):
        return

    await message.answer(texts.START_TEXT, reply_markup=keyboard.start_keyboard())


# ───── 🎲 ─────
@dp.message(F.dice)
async def dice_handler(message: Message):
    if message.chat.id != GROUP_ID:
        return

    # 🚫 Пересланный кубик
    if (
        message.forward_date
        or message.forward_from
        or message.forward_from_chat
        or message.forward_sender_name
    ):
        await message.reply(
            texts.FAIR_PLAY_TEXT,
            reply_markup=keyboard.memslots_keyboard()
        )
        return

    if is_banned(message.from_user.id):
        try: await message.delete()
        except: pass
        return

    if not antispam(message.from_user.id):
        await message.reply(texts.ANTISPAM_TEXT, reply_markup=keyboard.memslots_keyboard())
        return

    await asyncio.sleep(4)

    db = load_db()
    uid = str(message.from_user.id)
    roll = message.dice.value
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    username = message.from_user.username or f"id{uid}"

    player = db["players"].get(uid) or {
        "username": username,
        "balance": 0,
        "first": now,
        "last": now,
        "rolls": 0
    }

    player["balance"] += roll
    player["last"] = now
    player["rolls"] += 1
    db["players"][uid] = player
    save_db(db)

    await message.reply(
        texts.RESULTS_TEXT.format(roll=roll, balance=player["balance"]),
        reply_markup=keyboard.memslots_keyboard()
    )


# ───── /balance ─────
@dp.message(Command("balance"))
async def balance_cmd(message: Message):
    if message.chat.id != GROUP_ID:
        return

    if is_banned(message.from_user.id):
        try: await message.delete()
        except: pass
        return

    db = load_db()
    balance = db["players"].get(str(message.from_user.id), {}).get("balance", 0)
    await message.reply(texts.BALANCE_TEXT.format(balance=balance), reply_markup=keyboard.memslots_keyboard())


# ───── /statistics ─────
@dp.message(Command("statistics"))
async def stats_cmd(message: Message):
    if message.chat.id != GROUP_ID:
        return

    if is_banned(message.from_user.id):
        try: await message.delete()
        except: pass
        return

    db = load_db()
    p = db["players"].get(str(message.from_user.id))
    if not p:
        return
    await message.reply(texts.STATISTICS_TEXT.format(**p), reply_markup=keyboard.memslots_keyboard())


# ───── /top ─────
@dp.message(Command("top"))
async def top_cmd(message: Message):
    if message.chat.id != GROUP_ID:
        return

    if is_banned(message.from_user.id):
        try: await message.delete()
        except: pass
        return

    db = load_db()
    top = sorted(db["players"].values(), key=lambda x: x["balance"], reverse=True)[:5]
    text = texts.TOP_HEADER
    for i, p in enumerate(top, 1):
        text += f"{i}. @{p['username']} - <b>{p['balance']} 🧅</b>\n"

    await message.reply(text, reply_markup=keyboard.memslots_keyboard())


# ───── ADMIN COMMANDS ─────
@dp.message(F.text.startswith("/"))
async def admin_cmd(message: Message):
    if message.chat.id != GROUP_ID:
        return

    if not is_admin(message.from_user.id):
        try: await message.delete()
        except: pass
        return

    db = load_db()
    args = message.text.split()
    if len(args) < 2:
        return

    username = args[1].lstrip("@")
    target = next((uid for uid, p in db["players"].items() if p["username"] == username), None)
    if not target:
        await message.reply(texts.PLAYER_NOT_FOUND, reply_markup=keyboard.memslots_keyboard())
        return

    uid_int = int(target)
    cmd = args[0]

    if cmd == "/ban":
        if uid_int not in db["banned"]:
            db["banned"].append(uid_int)
        save_db(db)
        await message.reply(texts.BAN_DONE, reply_markup=keyboard.memslots_keyboard())
        return

    if cmd == "/unban":
        if uid_int in db["banned"]:
            db["banned"].remove(uid_int)
            save_db(db)
            await message.reply(texts.UNBAN_DONE, reply_markup=keyboard.memslots_keyboard())
        else:
            await message.reply(texts.UNBAN_NOT_BANNED, reply_markup=keyboard.memslots_keyboard())
        return

    if cmd == "/give":
        db["players"][target]["balance"] += int(args[2])
    elif cmd == "/del":
        db["players"][target]["balance"] -= int(args[2])
    elif cmd == "/reset":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"reset:{target}"),
             InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ])
        await message.reply(texts.RESET_CONFIRM, reply_markup=kb)
        return

    save_db(db)
    await message.reply(texts.ADMIN_DONE, reply_markup=keyboard.memslots_keyboard())


# ───── CALLBACKS ─────
@dp.callback_query(F.data.startswith("reset:"))
async def reset_confirm(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        await call.answer(texts.RESET_DENY, show_alert=True)
        return

    uid = call.data.split(":")[1]
    db = load_db()
    db["players"][uid]["balance"] = 0
    save_db(db)
    await call.message.edit_text(texts.RESET_DONE)


@dp.callback_query(F.data == "cancel")
async def reset_cancel(call: CallbackQuery):
    await call.message.edit_text(texts.RESET_CANCEL)


# ───── RUN ─────
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())