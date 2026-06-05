import asyncio
from pyrogram import Client
from pyrogram.raw.functions.messages import SendScreenshotNotification

async def main():
    SESSION_NAME = "ScreenNotProd" #session || testsession
    api_id = 23760924
    api_hash = "1479ed9dfb38ac82f7c3c31c692796ce"

    app = Client(
        SESSION_NAME,
        api_id=api_id,
        api_hash=api_hash,
        test_mode=False)

    async with app:
        peer_input = input("Введите ID/Username для отправки ScreenshotNotification: ")
        try:
            count = int(input("Введите количество ScreenshotNotification: "))
        except ValueError:
            print("Количество должно быть числом!")
            return

        peer = await app.resolve_peer(peer_input)

        print("Отправка началась...\n")

        for i in range(count):
            try:
                await app.invoke(
                    SendScreenshotNotification(
                        peer=peer,
                        reply_to_msg_id=0,
                        random_id=app.rnd_id()
                    )
                )
                print(f"Уведомление {i+1}/{count} отправлено")
#                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Ошибка на {i+1}: {e}")
                break

        print("\nГотово! ScreenshotNotification успешно отправлены!")

asyncio.run(main())