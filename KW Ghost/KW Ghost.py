import asyncio
import logging
import aiohttp
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, Update
from aiogram.filters import Command

# ========== НАСТРОЙКИ ==========
API_TOKEN = "8933864641:AAGgEbcW8TsiQRxbxaqNWWas5qeiyJO5WA4"  # Замените на ваш токен от @BotFather
MONITOR_CHAT_ID = -1003969020799  # ID вашей супергруппы
YOUR_TELEGRAM_ID = 969434663  # ⚠️ ВАШ ID в Telegram (узнайте у @userinfobot)

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== ИНИЦИАЛИЗАЦИЯ БОТА ==========
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хранилище сообщений
tracked_messages = {}

async def send_notification(chat_id: int, text: str):
    """Отправляет уведомление в указанную группу"""
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        logger.info(f"✅ Уведомление отправлено")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки: {e}")

def is_message_from_me(message: Message) -> bool:
    """Проверяет, отправил ли сообщение ВЫ"""
    if not message.from_user:
        return False
    # Сообщение от бота (бот действует от вашего имени)
    if message.from_user.is_bot:
        return True
    # Сообщение от вас лично
    if message.from_user.id == YOUR_TELEGRAM_ID:
        return True
    return False

def get_user_name(message: Message) -> str:
    """Возвращает имя пользователя"""
    if message.from_user:
        if message.from_user.username:
            return f"@{message.from_user.username}"
        return message.from_user.full_name
    return "Неизвестный"

# ========== ОСНОВНЫЕ ОБРАБОТЧИКИ ==========

# 1. Новые бизнес-сообщения
@dp.message(F.business_connection_id)
async def handle_business_message(message: Message):
    """Сохраняет новые сообщения ТОЛЬКО от собеседника"""
    try:
        if is_message_from_me(message):
            logger.info(f"⏭️ Пропущено своё сообщение")
            return
        
        # Получаем текст
        if message.text:
            msg_text = message.text
        elif message.caption:
            msg_text = f"[С подписью] {message.caption}"
        else:
            msg_text = f"[{message.content_type}]"
        
        # Сохраняем
        key = f"{message.chat.id}_{message.message_id}"
        tracked_messages[key] = {
            'text': msg_text,
            'user': get_user_name(message),
            'user_id': message.from_user.id,
            'date': message.date,
            'business_connection_id': message.business_connection_id
        }
        
        logger.info(f"📥 Сохранено сообщение от {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")

# 2. Изменённые бизнес-сообщения
@dp.edited_business_message()
async def handle_edited_business_message(message: Message):
    """Отслеживает ИЗМЕНЕНИЯ сообщений собеседника"""
    try:
        if is_message_from_me(message):
            logger.info(f"⏭️ Пропущено изменение своего сообщения")
            return
        
        key = f"{message.chat.id}_{message.message_id}"
        
        if key in tracked_messages:
            original = tracked_messages[key]
            old_text = original['text']
            new_text = message.text or message.caption or "[Медиа]"
            
            if old_text != new_text:
                notification = (
                    f"✏️ <b>СОБЕСЕДНИК ИЗМЕНИЛ СООБЩЕНИЕ</b>\n\n"
                    f"👤 <b>Пользователь:</b> {original['user']}\n"
                    f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
                    f"🕐 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"📝 <b>Было:</b>\n<code>{old_text[:500]}</code>\n\n"
                    f"📝 <b>Стало:</b>\n<code>{new_text[:500]}</code>"
                )
                await send_notification(MONITOR_CHAT_ID, notification)
                tracked_messages[key]['text'] = new_text
                logger.info(f"✏️ Обновлено сообщение")
        else:
            logger.info(f"Сообщение не найдено в кэше")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")

# 3. Удалённые сообщения - через отдельный хендлер на ALL updates
# ВНИМАНИЕ: В старых версиях aiogram нет нормальной поддержки удалений,
# поэтому будем обрабатывать это через getUpdates или raw_update

# Альтернативный способ: обрабатываем все updates через raw_update
@dp.update()
async def handle_all_updates(update: Update):
    """Обрабатывает все обновления, включая удалённые сообщения"""
    try:
        # Проверяем, есть ли в update поле deleted_business_messages
        if hasattr(update, 'deleted_business_messages') and update.deleted_business_messages:
            event = update.deleted_business_messages
            
            logger.info(f"🗑️ Обнаружено удаление {len(event.message_ids)} сообщений")
            
            notification = (
                f"🗑️ <b>СОБЕСЕДНИК УДАЛИЛ СООБЩЕНИЯ</b>\n\n"
                f"💬 <b>Чат ID:</b> <code>{event.chat.id}</code>\n"
                f"🕐 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"📋 <b>Удалены:</b>\n"
            )
            
            deleted_count = 0
            for msg_id in event.message_ids[:30]:
                key = f"{event.chat.id}_{msg_id}"
                if key in tracked_messages:
                    msg_data = tracked_messages[key]
                    notification += f"\n• <b>ID {msg_id}</b> (от {msg_data['user']}):\n  <code>{msg_data['text'][:150]}</code>"
                    del tracked_messages[key]
                    deleted_count += 1
                else:
                    notification += f"\n• <b>ID {msg_id}</b> (не отслеживалось)"
            
            if len(event.message_ids) > 30:
                notification += f"\n\n... и ещё {len(event.message_ids) - 30}"
            
            if deleted_count > 0:
                await send_notification(MONITOR_CHAT_ID, notification)
                logger.info(f"📤 Отправлено уведомление об удалении")
                
    except Exception as e:
        logger.error(f"Ошибка в handle_all_updates: {e}")

# ========== КОМАНДЫ ДЛЯ ГРУППЫ ==========

@dp.message(F.chat.id == MONITOR_CHAT_ID, Command("test"))
async def test_command(message: Message):
    await message.reply(
        f"✅ <b>Бот работает!</b>\n\n"
        f"📊 В кэше: {len(tracked_messages)} сообщений собеседника\n"
        f"👤 Ваш ID: <code>{YOUR_TELEGRAM_ID}</code>",
        parse_mode="HTML"
    )

@dp.message(F.chat.id == MONITOR_CHAT_ID, Command("stats"))
async def stats_command(message: Message):
    await message.reply(
        f"📊 <b>Статистика</b>\n\n"
        f"📝 Отслеживается: {len(tracked_messages)} сообщений",
        parse_mode="HTML"
    )

@dp.message(F.chat.id == MONITOR_CHAT_ID, Command("clear"))
async def clear_command(message: Message):
    global tracked_messages
    count = len(tracked_messages)
    tracked_messages = {}
    await message.reply(f"🗑️ Очищено {count} сообщений")

# ========== ЗАПУСК ==========
async def main():
    logger.info("🚀 Бот мониторинга запущен")
    logger.info(f"👤 Ваш ID: {YOUR_TELEGRAM_ID} (свои сообщения игнорируются)")
    
    # Отправляем приветствие
    await send_notification(
        MONITOR_CHAT_ID,
        f"✅ <b>Бот мониторинга запущен!</b>\n\n"
        f"👤 Ваш ID: <code>{YOUR_TELEGRAM_ID}</code>\n"
        f"⏭️ Свои сообщения ИГНОРИРУЮТСЯ\n\n"
        f"📌 Отслеживаются ТОЛЬКО сообщения СОБЕСЕДНИКА:\n"
        f"• ✏️ Изменения\n"
        f"• 🗑️ Удаления (через raw update)\n\n"
        f"<b>Команды:</b> /test, /stats, /clear"
    )
    
    # Запускаем с allowed_updates, включая deleted_business_messages
    await dp.start_polling(
        bot,
        allowed_updates=[
            "business_message",
            "edited_business_message", 
            "deleted_business_messages",
            "message",
            "edited_message"
        ]
    )

if __name__ == "__main__":
    asyncio.run(main())