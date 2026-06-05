# Если как то деобфусцировал и будешь это продавать. Ты уёбок.
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

blacklist_str = os.getenv('BLACKLIST', '')
blacklist = [int(id.strip()) for id in blacklist_str.split(',') if id.strip()] if blacklist_str else []
api_id = 23760924
api_hash = "1479ed9dfb38ac82f7c3c31c692796ce"


app = Client("ad", api_id=api_id, api_hash=api_hash, test_mode=True)

print("""
😶‍🌫️ Спасибо за покупку моего софта для рассылки постов КОНТАКТАМ в Telegram Test Server!
⌨️ Ответьте ".ad" на сообщение которое хотите разослать КОНТАКТАМ.

👤 Создатель - @kwiken (Test Server)
👤 Создатель - @kwiken_lab (Productive Server)

⚠️ Продажа запрещена!
❗️ Если вам продал этот софт кто либо другой сообщите мне.

🍀 Удачного пользование!
    """)

@app.on_message(filters.me & filters.command("ad", prefixes="."))
async def send_ad(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit_text("<emoji id=5370585277679009793>👨‍💻</emoji> Ответь этой командой на пост в канале для рассылки.")
        return
    ad_message = message.reply_to_message
    await message.edit_text("<emoji id=5373164573043982337>✅</emoji> Начинаем рассылку.")

    successful = 0
    errors = 0
    total_users = 0

    print("📢 Начинаем рассылку.\n\n")
    try:
        contacts = await client.get_contacts()
    except Exception as e:
        print(f"⚠️ Ошибка получения контактов: {e}")
        await message.edit_text(f"⚠️ Ошибка получения контактов: {e}")
        return
    if hasattr(contacts, 'users'):
        users = contacts.users
    else:
        users = contacts

    for user in users:
        if user.id not in blacklist and not user.is_bot:
            total_users += 1
            print(f"⚡️ Отправка пользователю {user.id} ({user.first_name or 'Unknown'})")
            try:
                await ad_message.forward(user.id)
                successful += 1
            except FloodWait as e:
                print(f"⌚️ FloodWait: ждём {e.value} секунд")
                await asyncio.sleep(e.value)
                try:
                    await ad_message.forward(user.id)
                    successful += 1
                except Exception as ex:
                    print(f"⚠️ Ошибка после flood: {ex}")
                    errors += 1
            except Exception as e:
                print(f"⚠️ Ошибка отправки {user.id}: {e}")
                errors += 1
            await asyncio.sleep(5)

    stats_text = f"""
    <emoji id=5373164573043982337>✅</emoji> Рассылка завершена.
     <emoji id=5370768814516469761>🕸</emoji> Всего пользователей: {total_users}
     <emoji id=5372861700540203009>⭐️</emoji> Успешно: {successful}
     <emoji id=5370585277679009793>👨‍💻</emoji> Ошибок: {errors}
    """
    await message.edit_text(stats_text)
    print(stats_text)

app.run()