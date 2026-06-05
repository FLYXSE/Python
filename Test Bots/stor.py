import asyncio
import random
import sys

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.stories import SendStoryRequest
from telethon.tl.types import InputMediaUploadedPhoto, InputPeerSelf, InputPrivacyValueAllowAll

# Замените на ваши значения из my.telegram.org

api_id = 23760924
api_hash = '1479ed9dfb38ac82f7c3c31c692796ce'
session_name = '14064389351'  # Имя сессии, будет сохранено в файл .session
test_dc_id = 2
test_ip = '149.154.167.40'
test_port = 80

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = TelegramClient(session_name, api_id, api_hash)
client.session.set_dc(test_dc_id, test_ip, test_port)

def get_inputs():
    print("Сбор входных данных...")
    num = int(input("Введите количество сторис: "))
    caption = input("Введите комментарий (caption): ")
    file_path = input("Введите путь к файлу (фото или видео) для всех сторис: ")
    print("Входные данные собраны.")
    return num, caption, file_path

async def async_input(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)

async def get_phone():
    return await async_input("Введите ваш номер телефона (или токен бота): ")

async def get_code():
    return await async_input("Введите код верификации: ")

async def get_password():
    return await async_input("Введите пароль (если требуется): ")

async def main(num, caption, file_path):
    print("Запуск клиента...")
    await client.start(
        phone=get_phone,
        code_callback=get_code,
        password=get_password
    )
    print("Клиент запущен и авторизован.")
    
    try:
        print("Начинаем публикацию сторис...")
        for i in range(num):
            print(f"Обработка сторис {i+1}/{num}...")
            while True:
                try:
                    print("Загрузка файла...")
                    uploaded_file = await client.upload_file(file_path)
                    print("Файл загружен.")
                    
                    media = InputMediaUploadedPhoto(file=uploaded_file)
                    privacy_rules = [InputPrivacyValueAllowAll()]
                    random_id = random.randint(0, 2**63 - 1)
                    
                    print("Отправка сторис...")
                    await client(SendStoryRequest(
                        peer=InputPeerSelf(),
                        media=media,
                        caption=caption,
                        privacy_rules=privacy_rules,
                        random_id=random_id,
                        pinned=True
                    ))
                    print(f"Сторис {i+1} опубликована.")
                    break
                except FloodWaitError as e:
                    wait_time = e.seconds + 1
                    print(f"Достигнут лимит: нужно подождать {wait_time} секунд из-за flood-wait.")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    print(f"Ошибка при публикации сторис {i+1}: {e}")
                    break  # Или continue для retry, но зависит от ошибки
            
            if i < num - 1:
                print("Задержка 1 секунд...")
                await asyncio.sleep(1)
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        print("Отключение клиента...")
        await client.disconnect()
        print("Клиент отключен.")

if __name__ == '__main__':
    num, caption, file_path = get_inputs()
    asyncio.run(main(num, caption, file_path))