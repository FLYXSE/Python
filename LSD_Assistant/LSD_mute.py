from pyrogram import Client, filters
from pyrogram.types import Message
from texts import *
from emoji import *
import json
import os


MUTE_FILE = "muted_users.json"


def load_muted():
    """Загрузка списка замученных пользователей"""
    if os.path.exists(MUTE_FILE):
        try:
            with open(MUTE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_muted(muted_list):
    """Сохранение списка замученных пользователей"""
    with open(MUTE_FILE, "w", encoding="utf-8") as f:
        json.dump(muted_list, f, ensure_ascii=False, indent=2)


async def mute(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.edit(LSD_mute_error)
            return

        arg = message.command[1].lower().strip()

        if arg == "+list":
            muted_list = load_muted()
            if not muted_list:
                await message.edit(LSD_mute_list_empty)
                return

            users_text = "\n".join([f"[{toch}] @{user}" for user in muted_list])
            result = LSD_mute_list.replace("[]", users_text)
            await message.edit(result)
            return

        # Удаление пользователя из мута
        if arg.startswith("-"):
            username = arg.lstrip("-@").lower()
            muted_list = load_muted()

            if username not in muted_list:
                await message.edit(LSD_mute_not_found.replace("[]", username))
                return

            muted_list.remove(username)
            save_muted(muted_list)

            await message.edit(LSD_mute_removed.replace("[]", username))
            return

        # Добавление пользователя в мут
        username = arg.lstrip("+@").lower()

        muted_list = load_muted()

        if username in muted_list:
            await message.edit(LSD_mute_already.replace("[]", username))
            return

        muted_list.append(username)
        save_muted(muted_list)

        await message.edit(LSD_mute_success.replace("[]", username))
    except Exception as e:
        await message.edit(f"Ошибка: {str(e)}")


async def check_muted_message(client: Client, message: Message):
    """Хендлер для автоудаления сообщений от замученных"""
    try:
        if not message.from_user:
            return

        # Проверяем только личные сообщения
        if message.chat.type != "private":
            return

        username = message.from_user.username
        if not username:
            return

        muted_list = load_muted()

        if username.lower() in muted_list:
            await message.delete(revoke=True)
    except Exception as e:
        print(f"Ошибка в check_muted_message: {e}")
