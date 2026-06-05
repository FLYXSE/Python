# CakeBOT - VildHelper X Clone (ALL METHODS FROM ORIGINAL)
# pip install --upgrade kurigram tgcrypto

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
import asyncio
import random
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

spam_active = {}

def create_client(session_name: str):
    app = Client(
        session_name,
        api_id=21592124,
        api_hash="c2100f2a2c6beb6af0a98830509f371a",
        test_mode=True,
    )

    # === .spam / .stopspam ===
    @app.on_message(filters.command("spam", prefixes=".") & filters.me)
    async def spam_command(client: Client, message: Message):
        spam_active[session_name] = True
        try: await message.delete()
        except: pass
        args = message.text.split(maxsplit=3)
        if len(args) < 4:
            return await client.send_message(message.chat.id, "<b>[X]</b> Формат: <code>.spam [кол-во] [задержка] [текст]</code>")
        try:
            count, delay, text = int(args[1]), float(args[2]), args[3]
        except: return await client.send_message(message.chat.id, "<b>[!]</b> Неверные аргументы")
        if count <= 0 or delay < 0:
            return await client.send_message(message.chat.id, "<b>[!]</b> Кол-во > 0, задержка ≥ 0")
        for i in range(count):
            if not spam_active.get(session_name, False): break
            try:
                await client.send_message(message.chat.id, text, reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None)
                if i < count - 1: await asyncio.sleep(delay)
            except Exception as e: break

    @app.on_message(filters.command("stopspam", prefixes=".") & filters.me)
    async def stop_spam(client, message):
        spam_active[session_name] = False
        await message.edit("<b>[OK]</b> Спам остановлен")

    # === .stars ===
    @app.on_message(filters.command("stars", prefixes=".") & filters.me)
    async def check_stars_balance(client: Client, message: Message):
        await message.edit("<b>[STAR]</b> Запрос баланса...")
        try:
            balance = await client.get_stars_balance()
            await message.edit(f"<b>Баланс звёзд:</b> <code>{balance}</code> ⭐", parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.edit(f"<b>[X]</b> Ошибка: <code>{e}</code>", parse_mode=ParseMode.HTML)

    # === .hide ===
    @app.on_message(filters.command("hide", prefixes=".") & filters.me)
    async def hide_cmd(client, message):
        limit = int(message.command[1]) if len(message.command) > 1 else None
        await message.edit("<b>[HIDDEN]</b> Скрываю подарки...")
        hidden = 0
        try:
            async for gift in client.get_chat_gifts("me"):
                if limit and hidden >= limit: break
                try: await gift.hide(); hidden += 1; await asyncio.sleep(0.1)
                except: continue
        except Exception as e:
            await message.edit("<b>[X]</b> Подарки недоступны. Используй .unhide")
            return
        await message.edit(f"<b>[OK]</b> Скрыто {hidden} подарков.")

    # === .unhide ===
    @app.on_message(filters.command("unhide", prefixes=".") & filters.me)
    async def unhide_cmd(client, message):
        limit = int(message.command[1]) if len(message.command) > 1 else None
        await message.edit("<b>[VISIBLE]</b> Показываю подарки...")
        shown = 0
        try:
            async for gift in client.get_chat_gifts("me"):
                if limit and shown >= limit: break
                try: await gift.show(); shown += 1; await asyncio.sleep(0.1)
                except: continue
        except Exception as e:
            await message.edit("<b>[X]</b> Подарки недоступны.")
            return
        await message.edit(f"<b>[OK]</b> Показано {shown} подарков.")

    # === .transfer — КАК В VILDHELPER (gift.transfer) ===
    @app.on_message(filters.command("transfer", ".") & filters.me)
    async def transfer_gifts(client, message):
        try:
            args = message.text.split(maxsplit=3)
            if len(args) < 3:
                await message.edit(
                    "<b>[X]</b> Формат: <code>.transfer @username количество [фон]</code>\n"
                    "Пример: <code>.transfer @giftsrelayer 1 Caramel</code>"
                )
                return

            username = args[1].lstrip("@")
            amount = int(args[2])
            if amount <= 0:
                await message.edit("<b>[X]</b> Количество > 0!")
                return
            background = args[3] if len(args) > 3 else None

            await message.edit(f"<b>[SEARCH]</b> Ищу подарки с фоном <code>{background or 'любым'}</code>...")

            matched_gifts = []
            try:
                async for gift in client.get_chat_gifts("me"):
                    backdrop_name = "Unknown"
                    try:
                        for attr in getattr(gift, 'attributes', []):
                            attr_type = str(getattr(attr, 'type', ''))
                            if "BACKDROP" in attr_type:
                                backdrop_name = getattr(attr, 'name', 'Unknown')
                                break
                    except: pass

                    if background and background.lower() not in backdrop_name.lower():
                        continue
                    matched_gifts.append(gift)
            except Exception as e:
                await message.edit(f"<b>[X]</b> Подарки недоступны: <code>{e}</code>")
                return

            if not matched_gifts:
                criteria = f" с фоном '{background}'" if background else ""
                await message.edit(f"<b>[X]</b> Не найдено подарков{criteria}.")
                return

            random.shuffle(matched_gifts)
            await message.edit(f"<b>[TRANSFER]</b> Передаю {min(amount, len(matched_gifts))} подарков @{username}...")

            transferred = 0
            errors = 0
            for gift in matched_gifts[:amount]:
                try:
                    await gift.transfer(username)
                    transferred += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    errors += 1
                    continue

            criteria_text = f" с фоном <code>{background}</code>" if background else ""
            report = (
                f"<b>[OK]</b> Успешно передал {transferred} подарков{criteria_text}\n"
                f"• Запрошено: {amount}\n"
                f"• Ошибок: {errors}\n"
                f"• Получатель: @{username}"
            )
            await message.edit(report, parse_mode=ParseMode.HTML)

        except Exception as ex:
            await message.edit(f"<b>[!]</b> Ошибка: {ex}")

    # === .giftstats — КАК В VILDHELPER ===
    @app.on_message(filters.command("giftstats", prefixes=".") & filters.me)
    async def gift_stats(client: Client, message: Message):
        await message.edit("<b>[STATS]</b> Анализ инвентаря...")

        models, backgrounds = {}, {}
        total = 0

        try:
            async for gift in client.get_chat_gifts("me"):
                total += 1
                for attr in getattr(gift, 'attributes', []):
                    attr_type_str = str(getattr(attr, 'type', ''))
                    attr_name = getattr(attr, 'name', 'Unknown')
                    if "MODEL" in attr_type_str:
                        models[attr_name] = models.get(attr_name, 0) + 1
                    elif "BACKDROP" in attr_type_str:
                        backgrounds[attr_name] = backgrounds.get(attr_name, 0) + 1
        except Exception as e:
            await message.edit(
                "<b>[X]</b> Подарки недоступны.\n"
                "<i>Попробуй:</i>\n"
                "• <code>.unhide</code>\n"
                "• Перезайди в аккаунт\n"
                "• Telegram Beta",
                parse_mode=ParseMode.HTML
            )
            return

        stats = f"<b>Ваши подарки:</b>\n<b>Всего:</b> <code>{total}</code>\n\n"
        if models:
            stats += "<b>Модели:</b>\n" + "\n".join(f"• {k}: {v}" for k, v in sorted(models.items())) + "\n"
        if backgrounds:
            stats += "<b>Фоны:</b>\n" + "\n".join(f"• {k}: {v}" for k, v in sorted(backgrounds.items()))
        if total == 0:
            stats += "<i>Подарков нет или они скрыты.</i>"

        await message.edit(stats, parse_mode=ParseMode.HTML)

    # === .coin ===
    @app.on_message(filters.command("coin", prefixes=".") & filters.me)
    async def flip_coin(client, message):
        result = random.choice(["Орёл", "Решка"])
        await message.edit(f"<b>Монетка:</b> <code>{result}</code>", parse_mode=ParseMode.HTML)

    # === .chatstats ===
    @app.on_message(filters.command("chatstats", prefixes=".") & filters.me)
    async def chat_stats(client: Client, message: Message):
        await message.edit("<b>[SYS]</b> Сбор статистики...")
        total_messages = total_media = 0
        user_activity = {}
        try:
            async for msg in client.get_chat_history(message.chat.id, limit=10000):
                total_messages += 1
                if msg.media: total_media += 1
                user = msg.from_user or msg.sender_chat
                if user:
                    uid = user.id
                    name = getattr(user, 'first_name', '') or getattr(user, 'title', 'Без имени')
                    user_activity[uid] = user_activity.get(uid, {'count': 0, 'name': name})
                    user_activity[uid]['count'] += 1
            top = sorted(user_activity.items(), key=lambda x: x[1]['count'], reverse=True)[:5]
            top_text = "\n".join(f"• <a href='tg://user?id={uid}'>{data['name']}</a>: <code>{data['count']}</code>" if uid > 0 else f"• {data['name']}: <code>{data['count']}</code>" for uid, data in top) if top else "Нет"
            await message.edit(f"<b>Статистика:</b>\nСообщений: <code>{total_messages}</code>\nМедиа: <code>{total_media}</code>\n<b>Топ-5:</b>\n{top_text}", parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.edit(f"<b>[X]</b> Ошибка: <code>{str(e)[:100]}</code>")

    # === .help ===
    @app.on_message(filters.command("help", prefixes=".") & filters.me)
    async def help_cmd(client, message):
        await message.edit("""
<b><i>CakeBOT</i></b> 
<code>.stars</code> — звёзды
<code>.hide</code> — скрыть
<code>.unhide</code> — показать
<code>.transfer @user N [фон]</code> — передать
<i>Пример: <code>.transfer @giftsrelayer 1 Caramel</code></i>
<code>.giftstats</code> — статистика
<code>.coin</code> — монетка
<code>.spam N 0.5 текст</code> — спам
<code>.stopspam</code> — стоп
<code>.chatstats</code> — чат
        """, parse_mode=ParseMode.HTML)

    return app

# === ЗАПУСК ===
async def main():
    print(r"""
   _____     _        _____
  / ____|   | |      |  __ \
 | |    __ _| | ___  | |__) | ___  _ __
 | |   / _` | |/ _ \ |  _  / / _ \| '_ \
 | |___| (_| | |  __/ | | \ \ (_) | |_) |
  \_____\__,_|_|\___| |_|  \_\___/| .__/
                                  | |
                                  |_|
    """)
    print("CakeBOT запущен. Введите имя сессии (например: cake1)\n")

    session_name = input("Имя сессии: ").strip() or "cakebot"
    app = create_client(session_name)

    print(f"Запуск {session_name}...")
    await app.start()

    me = await app.get_me()
    print(f"Успешно вошёл как: @{me.username or me.first_name}")

    print("CakeBOT готов. Используйте .help в Telegram Beta!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())