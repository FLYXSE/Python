from telethon import TelegramClient
from telethon.tl.types import User, Channel
import asyncio
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spam_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Настройки
API_ID = '23760924' # Тут вводите api_id с my.telegram.org
API_HASH = '1479ed9dfb38ac82f7c3c31c692796ce' # Тут вводите api_hash с my.telegram.org
MESSAGE_TEXT = '''глянь чё тут @KWTempMail_bot
'''
DELAY_BETWEEN_MESSAGES = 2  # Задержка между сообщениями в секундах

async def main():
    # Запрос номера телефона при запуске
    phone_number = input("Введите номер телефона: ").strip()
    
    client = TelegramClient('Test DC', API_ID, API_HASH)
    client.session.set_dc(2, '149.154.167.40', 80)
    await client.start(phone_number)
    
    logging.info("Начинаем процесс рассылки...")
    logging.info(f"Установлена задержка между сообщениями: {DELAY_BETWEEN_MESSAGES} секунд")

    dialogs = await client.get_dialogs()
    total_dialogs = len(dialogs)
    successful_sends = 0
    failed_sends = 0
    skipped_dialogs = 0
    
    logging.info(f"Найдено {total_dialogs} диалогов для обработки")
    
    for i, dialog in enumerate(dialogs, 1):
        entity = dialog.entity
        
        # Пропускаем если entity None
        if entity is None:
            skipped_dialogs += 1
            logging.info(f"[{i}/{total_dialogs}] Пропускаем диалог без entity")
            continue
            
        # Пропускаем только ботов
        if isinstance(entity, User) and entity.bot:
            skipped_dialogs += 1
            logging.info(f"[{i}/{total_dialogs}] Пропускаем бота: {entity.first_name}")
            continue
            
        # Для всех остальных диалогов пытаемся отправить сообщение
        try:
            # Отправляем сообщение
            await client.send_message(
                entity.id,
                MESSAGE_TEXT,
                parse_mode='html'
            )
            successful_sends += 1
            name = entity.title if hasattr(entity, 'title') else entity.first_name
            logging.info(f"[{i}/{total_dialogs}] Успешно отправлено в: {name}")
            
            # Задержка между сообщениями
            if i < total_dialogs:
                logging.info(f"Ожидание {DELAY_BETWEEN_MESSAGES} секунд перед следующей отправкой...")
                await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
                
        except Exception as e:
            failed_sends += 1
            name = entity.title if hasattr(entity, 'title') else entity.first_name
            logging.error(f"[{i}/{total_dialogs}] Ошибка отправки в {name}: {str(e)}")
            continue

    # Отчет о завершении
    logging.info("="*50)
    logging.info("Рассылка успешно завершена!")
    logging.info(f"Всего чатов на аккаунте: {total_dialogs}")
    logging.info(f"Успешных отправок: {successful_sends}")
    logging.info(f"Неудачных отправок: {failed_sends}")
    logging.info(f"Пропущено (боты): {skipped_dialogs}")
    logging.info("="*50)

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())