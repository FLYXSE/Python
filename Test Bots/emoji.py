# Исправленный UserBot для Telegram с Pyrogram.
# Отправляет два сообщения с премиум кастомными эмодзи по команде .test.

# Установите Pyrogram: pip install pyrogram

from pyrogram import Client, filters
from pyrogram.types import MessageEntity
from pyrogram.enums import MessageEntityType

# Замените на ваши API ID и Hash с my.telegram.org
api_id = 23760924
api_hash = "1479ed9dfb38ac82f7c3c31c692796ce"

app = Client("ad", api_id=api_id, api_hash=api_hash, test_mode=True)

successful = 0
errors = 0
total_users = 0


stats_text = f"""
    <emoji id=5373164573043982337>✅</emoji> Рассылка завершена.
     <emoji id=5370768814516469761>🕸</emoji> Всего пользователей: {total_users}
     <emoji id=5372861700540203009>⭐️</emoji> Успешно: {successful}
     <emoji id=5370585277679009793>👨‍💻</emoji> Ошибок: {errors}
    """

@app.on_message(filters.me & filters.command("test", prefixes="."))
async def test_command(client, message):
    # Первое сообщение
    text1 = "<emoji id=5373164573043982337>✅</emoji> Test"
    await message.edit_text(stats_text)

app.run()