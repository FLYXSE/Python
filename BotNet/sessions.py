import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    AuthKeyUnregistered,
    FloodWait,
    UserNotParticipant,
    PeerIdInvalid,
    BadRequest
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

API_ID = 21592124
API_HASH = "c2100f2a2c6beb6af0a98830509f371a"
TEST_MODE = True

BOT_TOKEN = "8347025481:AAGrxhOuiyIQduEqwabSFtFFGSNlVFBFkEo"

bot = Client(
    "telegram_session_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=SESSIONS_DIR
)

user_states = {}

STATE_NONE = "NONE"
STATE_ADD_ACCOUNT_PHONE = "ADD_ACCOUNT_PHONE"
STATE_ADD_ACCOUNT_CODE = "ADD_ACCOUNT_CODE"
STATE_ADD_ACCOUNT_PASSWORD = "ADD_ACCOUNT_PASSWORD"
STATE_DELETE_SESSION_CHOICE = "DELETE_SESSION_CHOICE"
STATE_BROADCAST_TEXT = "BROADCAST_TEXT"
STATE_BROADCAST_TARGET = "BROADCAST_TARGET"
STATE_BROADCAST_COUNT = "BROADCAST_COUNT"
STATE_SUBSCRIBE_CHANNEL = "SUBSCRIBE_CHANNEL"
STATE_SET_NAME_FIRST = "SET_NAME_FIRST"
STATE_SET_NAME_LAST = "SET_NAME_LAST"
STATE_SET_USERNAME = "SET_USERNAME"
STATE_SET_BIO = "SET_BIO"
STATE_LEAVE_CHATS_CONFIRM = "LEAVE_CHATS_CONFIRM"


def create_client(session_name):
    return Client(
        name=session_name,
        api_id=API_ID,
        api_hash=API_HASH,
        test_mode=TEST_MODE,
        workdir=SESSIONS_DIR,
        sleep_threshold=30
    )

def get_session_path(session_name):
    return os.path.join(SESSIONS_DIR, session_name + ".session")

def get_phone_from_session_name(session_name):
    return "+" + session_name.replace("account_", "")

def get_session_name_from_phone(phone):
    return f"account_{phone[1:]}"


@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_states.pop(message.from_user.id, None)
    await message.reply(
        "Привет! Я бот для управления Telegram аккаунтами.\n\n"
        "Доступные команды:\n"
        "/add_account - Добавить новый лук\n"
        "/list_sessions - Показать список сохраненных луков\n"
        "/delete_session - Удалить лук\n"
        "/broadcast - Раssылk@ луками\n"
        "/subscribe - Подписать луки\n"
        "/set_name - Новое имя всем лукам\n"
        "/set_username - Новый username всем лукам\n"
        "/set_bio - Новый 'о себе' всем лукам\n"
        "/check_accounts - Проверить активность луков\n"
        "/get_info - Получить ID и username луков\n"
        "/leave_chats - Выйти из всех чатов (осторожно!)\n"
    )

@bot.on_message(filters.command("add_account") & filters.private)
async def add_account_command(client, message):
    user_states[message.from_user.id] = {'state': STATE_ADD_ACCOUNT_PHONE}
    await message.reply("Введите номер телефона с '+' (например +9996661234):")

@bot.on_message(filters.command("list_sessions") & filters.private)
async def list_sessions_command(client, message):
    user_states.pop(message.from_user.id, None)
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков.")
        return

    response = "-- Сохраненные аккаунты --\n"
    for i, name in enumerate(sessions, 1):
        phone = get_phone_from_session_name(name)
        response += f"{i}. {phone}\n"
    await message.reply(response)

@bot.on_message(filters.command("delete_session") & filters.private)
async def delete_session_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для удаления.")
        return

    keyboard = []
    for i, name in enumerate(sessions, 1):
        phone = get_phone_from_session_name(name)
        keyboard.append([InlineKeyboardButton(f"{i}. {phone}", callback_data=f"delete_session_{i-1}")])
    
    user_states[message.from_user.id] = {'state': STATE_DELETE_SESSION_CHOICE, 'data': {'sessions': sessions}}
    await message.reply("Выберите лук для удаления:", reply_markup=InlineKeyboardMarkup(keyboard))

@bot.on_callback_query(filters.regex(r"delete_session_(\d+)"))
async def delete_session_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in user_states or user_states[user_id]['state'] != STATE_DELETE_SESSION_CHOICE:
        await callback_query.answer("Эта операция устарела или недействительна.", show_alert=True)
        return

    choice_index = int(callback_query.data.split('_')[-1])
    sessions = user_states[user_id]['data']['sessions']

    if choice_index < 0 or choice_index >= len(sessions):
        await callback_query.answer("Ошибка: неверный номер.", show_alert=True)
        return

    session_name = sessions[choice_index]
    phone = get_phone_from_session_name(session_name)
    session_path = get_session_path(session_name)

    try:
        os.remove(session_path)
        await callback_query.edit_message_text(f"Лук {phone} удалена.")
    except Exception as e:
        await callback_query.edit_message_text(f"Ошибка при удалении лука {phone}: {e}")
    finally:
        user_states.pop(user_id, None)

@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для Раssылkи.")
        return
    user_states[message.from_user.id] = {'state': STATE_BROADCAST_TEXT, 'data': {'sessions': sessions}}
    await message.reply("Введите сообщения для Раssылk:")

@bot.on_message(filters.command("subscribe") & filters.private)
async def subscribe_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для подписки.")
        return
    user_states[message.from_user.id] = {'state': STATE_SUBSCRIBE_CHANNEL, 'data': {'sessions': sessions}}
    await message.reply("Введите username канала (например @news):")

@bot.on_message(filters.command("set_name") & filters.private)
async def set_name_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для смены имени.")
        return
    user_states[message.from_user.id] = {'state': STATE_SET_NAME_FIRST, 'data': {'sessions': sessions}}
    await message.reply("Введите новое имя:")

@bot.on_message(filters.command("set_username") & filters.private)
async def set_username_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для смены username.")
        return
    user_states[message.from_user.id] = {'state': STATE_SET_USERNAME, 'data': {'sessions': sessions}}
    await message.reply("Введите новый username (без @):")

@bot.on_message(filters.command("set_bio") & filters.private)
async def set_bio_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для обновления статуса.")
        return
    user_states[message.from_user.id] = {'state': STATE_SET_BIO, 'data': {'sessions': sessions}}
    await message.reply("Введите новый статус 'о себе':")

@bot.on_message(filters.command("check_accounts") & filters.private)
async def check_accounts_command(client, message):
    user_states.pop(message.from_user.id, None)
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для проверки.")
        return

    await message.reply(f"Начинаю проверку {len(sessions)} лука(ов)...")
    results = await _check_accounts(sessions)
    await message.reply(results)

@bot.on_message(filters.command("get_info") & filters.private)
async def get_info_command(client, message):
    user_states.pop(message.from_user.id, None)
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для получения информации.")
        return

    await message.reply(f"Собираю информацию о {len(sessions)} луке(ах)...")
    results = await _get_my_info(sessions)
    await message.reply(results)

@bot.on_message(filters.command("leave_chats") & filters.private)
async def leave_chats_command(client, message):
    sessions = await _list_sessions()
    if not sessions:
        await message.reply("Нет сохраненных луков для выхода из чатов.")
        return
    
    user_states[message.from_user.id] = {'state': STATE_LEAVE_CHATS_CONFIRM, 'data': {'sessions': sessions}}
    await message.reply(
        "ВНИМАНИЕ: все луки покинут ВСЕ чаты и каналы. "
        "Вы уверены, что хотите продолжить? Ответьте 'да' или 'нет'."
    )

@bot.on_message(filters.private & filters.text & ~filters.regex(r"^/"))
async def handle_state_messages(client, message):
    user_id = message.from_user.id
    current_state = user_states.get(user_id, {}).get('state', STATE_NONE)
    user_data = user_states.get(user_id, {}).get('data', {})

    if current_state == STATE_ADD_ACCOUNT_PHONE:
        phone = message.text.strip()
        if not phone.startswith("+") or not phone[1:].isdigit():
            await message.reply("Ошибка: номер должен начинаться с '+' и содержать только цифры. Попробуйте снова.")
            return

        session_name = get_session_name_from_phone(phone)
        client_account = create_client(session_name)
        user_states[user_id]['data'] = {'phone': phone, 'client': client_account, 'session_name': session_name}

        try:
            await client_account.connect()
            await message.reply("Отправка кода...")
            sent_code = await client_account.send_code(phone)
            user_states[user_id]['data']['sent_code'] = sent_code
            user_states[user_id]['state'] = STATE_ADD_ACCOUNT_CODE
            await message.reply("Введите код (5 цифр):")
        except PhoneNumberInvalid:
            await message.reply("Ошибка: неверный номер. Используйте тестовые номера.")
            await client_account.disconnect()
            user_states.pop(user_id, None)
        except FloodWait as e:
            await message.reply(f"Слишком много попыток. Подождите {e.value} секунд.")
            await client_account.disconnect()
            user_states.pop(user_id, None)
        except Exception as e:
            await message.reply(f"Ошибка: {e}")
            await client_account.disconnect()
            user_states.pop(user_id, None)

    elif current_state == STATE_ADD_ACCOUNT_CODE:
        code = message.text.strip()
        if not code.isdigit() or len(code) != 5:
            await message.reply("Ошибка: код должен быть из 5 цифр. Попробуйте снова.")
            return

        client_account = user_data['client']
        phone = user_data['phone']
        sent_code = user_data['sent_code']
        session_name = user_data['session_name']
        session_path = get_session_path(session_name)

        success = False
        try:
            await client_account.sign_in(phone, sent_code.phone_code_hash, code)
            success = True
        except SessionPasswordNeeded:
            user_states[user_id]['state'] = STATE_ADD_ACCOUNT_PASSWORD
            await message.reply("Требуется 2FA пароль. Введите пароль:")
            return
        except PhoneCodeInvalid:
            await message.reply("Ошибка: неверный код. Попробуйте снова.")
        except FloodWait as e:
            await message.reply(f"Слишком много попыток. Подождите {e.value} секунд.")
        except Exception as e:
            await message.reply(f"Ошибка: {e}")
        finally:
            if success:
                await message.reply(f"Лук {phone} успешно сохранен!")
                await client_account.disconnect()
                user_states.pop(user_id, None)
            elif not success and user_states.get(user_id, {}).get('state') != STATE_ADD_ACCOUNT_PASSWORD:
                await client_account.disconnect()
                if os.path.exists(session_path):
                    try:
                        os.remove(session_path)
                        await message.reply("Неудачный лук удален.")
                    except Exception as e:
                        await message.reply(f"Не удалось удалить файл лука: {e}")
                user_states.pop(user_id, None)

    elif current_state == STATE_ADD_ACCOUNT_PASSWORD:
        password = message.text.strip()
        client_account = user_data['client']
        session_name = user_data['session_name']
        session_path = get_session_path(session_name)
        phone = user_data['phone']

        success = False
        try:
            await client_account.check_password(password=password)
            success = True
            await message.reply(f"Лук {phone} успешно сохранен!")
        except Exception as e:
            await message.reply(f"Ошибка 2FA: {e}. Попробуйте снова.")
        finally:
            await client_account.disconnect()
            if not success and os.path.exists(session_path):
                try:
                    os.remove(session_path)
                    await message.reply("Неудачный лук удалён.")
                except Exception as e:
                    await message.reply(f"Не удалось удалить файл лука: {e}")
            user_states.pop(user_id, None)

    elif current_state == STATE_BROADCAST_TEXT:
        message_text = message.text.strip()
        if not message_text:
            await message.reply("Ошибка: сообщение не может быть пустым. Попробуйте снова.")
            return
        user_data['message_text'] = message_text
        user_states[user_id]['state'] = STATE_BROADCAST_TARGET
        await message.reply("Введите получателя (@username или ID):")

    elif current_state == STATE_BROADCAST_TARGET:
        target = message.text.strip()
        if not target:
            await message.reply("Ошибка: получатель не указан. Попробуйте снова.")
            return
        user_data['target'] = target
        user_states[user_id]['state'] = STATE_BROADCAST_COUNT
        await message.reply("Сколько раз отправить?")

    elif current_state == STATE_BROADCAST_COUNT:
        try:
            count = int(message.text.strip() or "1")
            if count < 1:
                count = 1
        except ValueError:
            count = 1
        user_data['count'] = count

        sessions = user_data['sessions']
        message_text = user_data['message_text']
        target = user_data['target']

        await message.reply(f"Начинаю Раssылky {count} сообщений с {len(sessions)} лука(ов)...")
        results = await _broadcast_message(sessions, message_text, target, count)
        await message.reply(results)
        user_states.pop(user_id, None)

    elif current_state == STATE_SUBSCRIBE_CHANNEL:
        channel = message.text.strip()
        if not channel.startswith("@"):
            channel = "@" + channel
        
        sessions = user_data['sessions']
        await message.reply(f"Начинаю подписку на {channel} с {len(sessions)} лука(ов)...")
        results = await _mass_subscribe(sessions, channel)
        await message.reply(results)
        user_states.pop(user_id, None)

    elif current_state == STATE_SET_NAME_FIRST:
        first_name = message.text.strip()
        if not first_name:
            await message.reply("Ошибка: имя не может быть пустым. Попробуйте снова.")
            return
        user_data['first_name'] = first_name
        user_states[user_id]['state'] = STATE_SET_NAME_LAST
        await message.reply("Введите фамилию:")

    elif current_state == STATE_SET_NAME_LAST:
        last_name = message.text.strip() or None
        user_data['last_name'] = last_name

        sessions = user_data['sessions']
        first_name = user_data['first_name']

        await message.reply(f"Начинаю смену имени для {len(sessions)} лука(ов)...")
        results = await _mass_set_username(sessions, first_name, last_name)
        await message.reply(results)
        user_states.pop(user_id, None)

    elif current_state == STATE_SET_USERNAME:
        base_username = message.text.strip().lstrip('@')
        if not base_username:
            await message.reply("Ошибка: username не может быть пустым. Попробуйте снова.")
            return
        
        sessions = user_data['sessions']
        await message.reply(f"Начинаю смену username для {len(sessions)} лука(ов)...")
        results = await _mass_set_username_sequential(sessions, base_username)
        await message.reply(results)
        user_states.pop(user_id, None)

    elif current_state == STATE_SET_BIO:
        bio = message.text.strip()
        if not bio:
            await message.reply("Ошибка: статус не может быть пустым. Попробуйте снова.")
            return
        
        sessions = user_data['sessions']
        await message.reply(f"Начинаю обновление 'о себе' для {len(sessions)} лука(ов)...")
        results = await _mass_set_bio(sessions, bio)
        await message.reply(results)
        user_states.pop(user_id, None)

    elif current_state == STATE_LEAVE_CHATS_CONFIRM:
        confirm = message.text.strip().lower()
        if confirm in ("y", "yes", "да"):
            sessions = user_data['sessions']
            await message.reply(f"Начинаю выход из всех чатов для {len(sessions)} лука(ов)...")
            results = await _leave_all_chats(sessions)
            await message.reply(results)
        else:
            await message.reply("Выход из чатов отменен.")
        user_states.pop(user_id, None)

    else:
        await message.reply("Неизвестная команда или неверное состояние. Используйте /start для начала.")


async def _list_sessions():
    try:
        files = os.listdir(SESSIONS_DIR)
        sessions = [f[:-8] for f in files if f.endswith(".session") and not f.startswith("telegram_session_manager_bot")]
        return sessions
    except Exception:
        return []

async def _broadcast_message(sessions, message_text, target, count):
    results = []
    async def send_from_session(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            for _ in range(count):
                await client_account.send_message(target, message_text)
            results.append(f"[OK] {phone}")
        except Exception as e:
            results.append(f"[FAIL] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [send_from_session(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _mass_subscribe(sessions, channel):
    results = []
    async def subscribe_from_session(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            await client_account.join_chat(channel)
            results.append(f"[OK] {phone}")
        except UserNotParticipant:
            results.append(f"[INFO] {phone} уже подписан или не может присоединиться.")
        except Exception as e:
            results.append(f"[FAIL] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [subscribe_from_session(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _mass_set_username(sessions, first_name, last_name):
    results = []
    async def update_name(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            await client_account.update_profile(first_name=first_name, last_name=last_name)
            results.append(f"[OK] {phone}")
        except Exception as e:
            results.append(f"[FAIL] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [update_name(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _mass_set_username_sequential(sessions, base_username):
    results = []
    async def update_username(session_name, index):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        
        if index == 0:
            target_username = base_username
        else:
            target_username = f"{base_username}_{index + 1}"
            
        try:
            await client_account.start()
            await client_account.set_username(target_username)
            results.append(f"[OK] {phone} -> @{target_username}")
        except BadRequest as e:
            if "USERNAME_INVALID" in str(e):
                results.append(f"[FAIL] {phone}: Неверный формат username (@{target_username}).")
            elif "USERNAME_OCCUPIED" in str(e):
                results.append(f"[FAIL] {phone}: Username @{target_username} уже занят.")
            else:
                results.append(f"[FAIL] {phone}: {e}")
        except Exception as e:
            results.append(f"[FAIL] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [update_username(s, i) for i, s in enumerate(sessions)]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _mass_set_bio(sessions, bio):
    results = []
    async def update_bio(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            await client_account.update_profile(bio=bio)
            results.append(f"[OK] {phone}")
        except Exception as e:
            results.append(f"[FAIL] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [update_bio(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _check_accounts(sessions):
    results = []
    async def check_session(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            me = await client_account.get_me()
            results.append(f"[ACTIVE] {phone} | {me.first_name}")
        except AuthKeyUnregistered:
            results.append(f"[DEAD] {phone}")
        except Exception as e:
            results.append(f"[ERROR] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [check_session(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _leave_all_chats(sessions):
    results = []
    async def leave_chats(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            me = await client_account.get_me()
            async for dialog in client_account.get_dialogs():
                try:
                    if dialog.chat.id in (777000, 42777, me.id):
                        continue
                    await client_account.leave_chat(dialog.chat.id, delete=True)
                except Exception:
                    pass
            results.append(f"[OK] {phone} вышел из всех чатов")
        except Exception as e:
            results.append(f"[FAIL] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [leave_chats(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

async def _get_my_info(sessions):
    results = []
    async def fetch_info(session_name):
        client_account = create_client(session_name)
        phone = get_phone_from_session_name(session_name)
        try:
            await client_account.start()
            me = await client_account.get_me()
            user_id = me.id
            username = f"@{me.username}" if me.username else "нет"
            results.append(f"[INFO] {phone} | ID: {user_id} | Username: {username}")
        except Exception as e:
            results.append(f"[ERROR] {phone}: {e}")
        finally:
            await client_account.stop()

    tasks = [fetch_info(s) for s in sessions]
    await asyncio.gather(*tasks, return_exceptions=True)
    return "\n".join(results)

if __name__ == "__main__":
    print("Запуск [🤖] Onion Bot")
    print("[🤖] Onion Bot запущен. Отправьте /start боту, чтобы начать.")
    bot.run()
    print("Бот остановлен.")