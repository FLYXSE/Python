from pyrogram import Client, filters
import asyncio
import logging
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid, UsernameInvalid, UsernameNotOccupied, ChannelPrivate, ChatAdminRequired

# Включаем логирование для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Чёрный список ID подарков, которые НЕЛЬЗЯ передавать (уникальные ID из ссылки типа Cake-426501 → 426501)
BLACKLIST_GIFT_IDS = set()

app = Client(
    "ad",
    api_id=21592124,
    api_hash="c2100f2a2c6beb6af0a98830509f371a",
    test_mode=True,
    plugins=dict(root="plugins")
)

@app.on_message(filters.command("transfer", ".") & filters.me)
async def transfer_nft(client, message):
    try:
        if len(message.command) < 3:
            await message.edit("❌ Неверный формат!\nИспользуйте: <code>.transfer юзернейм количество [тип_подарка]</code>\n\nДоступные типы: <code>Cake</code>, <code>Drink</code>, <code>Cat</code> или <code>all</code>")
            return

        username = message.command[1].lstrip("@")
        
        try:
            amount = int(message.command[2])
            if amount <= 0:
                await message.edit("❌ Количество должно быть положительным!")
                return
        except ValueError:
            await message.edit("❌ Укажите корректное количество!")
            return

        gift_type = None
        if len(message.command) >= 4:
            gift_type = message.command[3].lower()
            if gift_type not in ['cake', 'drink', 'cat', 'all']:
                await message.edit("❌ Неверный тип! Доступно: Cake, Drink, Cat, all")
                return

        type_text = "всех типов" if gift_type == 'all' or not gift_type else gift_type.capitalize()
        await message.edit(f"🔄 Начинаю передачу {amount} NFT ({type_text}) → @{username}...")

        transferred = 0
        errors = 0
        skipped_wrong_type = 0
        skipped_blacklist = 0
        
        async for nft in client.get_chat_gifts("me"):
            if transferred >= amount:
                break

            try:
                gift_name = getattr(nft, 'title', '').lower()
                gift_id = getattr(nft, 'id', None)

                if gift_id is None:
                    logger.warning("Подарок без ID — пропускаем проверку")
                elif gift_id in BLACKLIST_GIFT_IDS:
                    skipped_blacklist += 1
                    continue

                if gift_type and gift_type != 'all':
                    if gift_type == 'cake' and 'cake' not in gift_name:
                        skipped_wrong_type += 1
                        continue
                    elif gift_type == 'drink' and 'drink' not in gift_name:
                        skipped_wrong_type += 1
                        continue
                    elif gift_type == 'cat' and 'cat' not in gift_name:
                        skipped_wrong_type += 1
                        continue

                result = await nft.transfer(username)
                transferred += 1
                await asyncio.sleep(0.1)
                
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка передачи: {e}")
                continue

        report = (
            f"📊 Отчёт по передаче:\n\n"
            f"• Запрошено: {amount}\n"
            f"• Передано: {transferred}\n"
            f"• Ошибок: {errors}\n"
            f"• Пропущено (не тот тип): {skipped_wrong_type}\n"
            f"• Пропущено (чёрный список): {skipped_blacklist}\n"
            f"• Получатель: @{username}\n"
            f"• Тип: {type_text}"
        )

        await message.edit(report)

    except Exception as ex:
        await message.edit(f"⚠️ Ошибка: {ex}")
        logger.error(f"Ошибка в .transfer: {ex}")

# Аналогично для специализированных команд (cake, drink, cat)

@app.on_message(filters.command("transfer_cake", ".") & filters.me)
async def transfer_cake(client, message):
    try:
        if len(message.command) < 3:
            await message.edit("❌ Формат: <code>.transfer_cake юзернейм количество</code>")
            return

        username = message.command[1].lstrip("@")
        
        try:
            amount = int(message.command[2])
            if amount <= 0:
                await message.edit("❌ Количество > 0!")
                return
        except ValueError:
            await message.edit("❌ Некорректное количество!")
            return

        await message.edit(f"🎂 Передаю {amount} Cake → @{username}...")

        transferred = 0
        errors = 0
        skipped_wrong_type = 0
        skipped_blacklist = 0
        
        async for nft in client.get_chat_gifts("me"):
            if transferred >= amount:
                break

            try:
                gift_name = getattr(nft, 'title', '').lower()
                gift_id = getattr(nft, 'id', None)

                if gift_id is None:
                    logger.warning("Подарок без ID")
                elif gift_id in BLACKLIST_GIFT_IDS:
                    skipped_blacklist += 1
                    continue

                if 'cake' not in gift_name:
                    skipped_wrong_type += 1
                    continue

                result = await nft.transfer(username)
                transferred += 1
                await asyncio.sleep(0.1)
                
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка Cake: {e}")
                continue

        report = (
            f"📊 Отчёт Cake:\n\n"
            f"• Запрошено: {amount}\n"
            f"• Передано: {transferred}\n"
            f"• Ошибок: {errors}\n"
            f"• Пропущено (не Cake): {skipped_wrong_type}\n"
            f"• Пропущено (чёрный список): {skipped_blacklist}\n"
            f"• Получатель: @{username}"
        )

        await message.edit(report)

    except Exception as ex:
        await message.edit(f"⚠️ Ошибка: {ex}")
        logger.error(f"Ошибка .transfer_cake: {ex}")

@app.on_message(filters.command("transfer_drink", ".") & filters.me)
async def transfer_drink(client, message):
    try:
        if len(message.command) < 3:
            await message.edit("❌ Формат: <code>.transfer_drink юзернейм количество</code>")
            return

        username = message.command[1].lstrip("@")
        
        try:
            amount = int(message.command[2])
            if amount <= 0:
                await message.edit("❌ Количество > 0!")
                return
        except ValueError:
            await message.edit("❌ Некорректное количество!")
            return

        await message.edit(f"🍹 Передаю {amount} Drink → @{username}...")

        transferred = 0
        errors = 0
        skipped_wrong_type = 0
        skipped_blacklist = 0
        
        async for nft in client.get_chat_gifts("me"):
            if transferred >= amount:
                break

            try:
                gift_name = getattr(nft, 'title', '').lower()
                gift_id = getattr(nft, 'id', None)

                if gift_id is None:
                    logger.warning("Подарок без ID")
                elif gift_id in BLACKLIST_GIFT_IDS:
                    skipped_blacklist += 1
                    continue

                if 'drink' not in gift_name:
                    skipped_wrong_type += 1
                    continue

                result = await nft.transfer(username)
                transferred += 1
                await asyncio.sleep(0.1)
                
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка Drink: {e}")
                continue

        report = (
            f"📊 Отчёт Drink:\n\n"
            f"• Запрошено: {amount}\n"
            f"• Передано: {transferred}\n"
            f"• Ошибок: {errors}\n"
            f"• Пропущено (не Drink): {skipped_wrong_type}\n"
            f"• Пропущено (чёрный список): {skipped_blacklist}\n"
            f"• Получатель: @{username}"
        )

        await message.edit(report)

    except Exception as ex:
        await message.edit(f"⚠️ Ошибка: {ex}")
        logger.error(f"Ошибка .transfer_drink: {ex}")

@app.on_message(filters.command("transfer_cat", ".") & filters.me)
async def transfer_cat(client, message):
    try:
        if len(message.command) < 3:
            await message.edit("❌ Формат: <code>.transfer_cat юзернейм количество</code>")
            return

        username = message.command[1].lstrip("@")
        
        try:
            amount = int(message.command[2])
            if amount <= 0:
                await message.edit("❌ Количество > 0!")
                return
        except ValueError:
            await message.edit("❌ Некорректное количество!")
            return

        await message.edit(f"🐈 Передаю {amount} Cat → @{username}...")

        transferred = 0
        errors = 0
        skipped_wrong_type = 0
        skipped_blacklist = 0
        
        async for nft in client.get_chat_gifts("me"):
            if transferred >= amount:
                break

            try:
                gift_name = getattr(nft, 'title', '').lower()
                gift_id = getattr(nft, 'id', None)

                if gift_id is None:
                    logger.warning("Подарок без ID")
                elif gift_id in BLACKLIST_GIFT_IDS:
                    skipped_blacklist += 1
                    continue

                if 'cat' not in gift_name:
                    skipped_wrong_type += 1
                    continue

                result = await nft.transfer(username)
                transferred += 1
                await asyncio.sleep(0.1)
                
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка Cat: {e}")
                continue

        report = (
            f"📊 Отчёт Cat:\n\n"
            f"• Запрошено: {amount}\n"
            f"• Передано: {transferred}\n"
            f"• Ошибок: {errors}\n"
            f"• Пропущено (не Cat): {skipped_wrong_type}\n"
            f"• Пропущено (чёрный список): {skipped_blacklist}\n"
            f"• Получатель: @{username}"
        )

        await message.edit(report)

    except Exception as ex:
        await message.edit(f"⚠️ Ошибка: {ex}")
        logger.error(f"Ошибка .transfer_cat: {ex}")

@app.on_message(filters.command("gifts", ".") & filters.me)
async def check_gifts(client, message):
    try:
        await message.edit("🔄 Подсчитываю подарки/NFT...")
        
        total_gifts = 0
        gift_types = {}
        
        async for gift in client.get_chat_gifts("me"):
            total_gifts += 1
            gift_name = getattr(gift, 'title', 'Неизвестный')
            gift_types[gift_name] = gift_types.get(gift_name, 0) + 1
        
        if total_gifts == 0:
            report = "🎁 Нет подарков/NFT на аккаунте"
        else:
            report = f"🎁 **Статистика подарков:**\n\n**Всего:** {total_gifts}\n\n**По типам:**\n"
            for name, count in gift_types.items():
                report += f"• {name}: {count} шт.\n"
        
        await message.edit(report)
        
    except Exception as ex:
        await message.edit(f"⚠️ Ошибка: {ex}")
        logger.error(f"Ошибка .gifts: {ex}")

# Новые команды для чёрного списка

@app.on_message(filters.command(["bl", "blacklist"], ".") & filters.me)
async def blacklist_cmd(client, message):
    try:
        if len(message.command) == 1:
            # Показать список
            if not BLACKLIST_GIFT_IDS:
                await message.edit("Чёрный список пуст.")
                return
            bl_text = "\n".join(f"• {gid}" for gid in sorted(BLACKLIST_GIFT_IDS))
            await message.edit(f"📋 Чёрный список ({len(BLACKLIST_GIFT_IDS)}):\n{bl_text}\n\n<code>.bl 426501</code> — добавить\n<code>.unbl 426501</code> — удалить")
            return

        added = 0
        invalid = 0
        for arg in message.command[1:]:
            try:
                gid = int(arg.strip())
                if gid not in BLACKLIST_GIFT_IDS:
                    BLACKLIST_GIFT_IDS.add(gid)
                    added += 1
            except ValueError:
                invalid += 1

        msg = f"✅ Добавлено: {added}\n"
        if invalid:
            msg += f"❌ Неверный формат: {invalid}\n"
        msg += "Пример: <code>.bl 426501 123456</code>"
        await message.edit(msg)

    except Exception as ex:
        await message.edit(f"Ошибка: {ex}")

@app.on_message(filters.command(["unbl", "blremove", "unblacklist"], ".") & filters.me)
async def unblacklist_cmd(client, message):
    try:
        if len(message.command) < 2:
            await message.edit("Укажите ID: <code>.unbl 426501</code>")
            return

        removed = 0
        for arg in message.command[1:]:
            try:
                gid = int(arg)
                if gid in BLACKLIST_GIFT_IDS:
                    BLACKLIST_GIFT_IDS.remove(gid)
                    removed += 1
            except ValueError:
                pass

        await message.edit(f"🗑 Удалено из чёрного списка: {removed} ID")
    except Exception as ex:
        await message.edit(f"Ошибка: {ex}")

HELP_TEXT = """
<b>📜 NFT Giver V2.3 (с чёрным списком) — @MACTEPCTBO</b>

<code>.transfer [юзер] [кол-во] [тип/all]</code> — универсальная передача
<code>.transfer_cake [юзер] [кол-во]</code>
<code>.transfer_drink [юзер] [кол-во]</code>
<code>.transfer_cat [юзер] [кол-во]</code>

<code>.gifts</code> — статистика подарков

<code>.bl</code> — показать чёрный список
<code>.bl 426501 12345</code> — добавить ID в чёрный список
<code>.unbl 426501</code> — удалить ID из чёрного списка
"""

@app.on_message(filters.command("help", ".") & filters.me)
async def help_cmd(client, message):
    await message.edit(HELP_TEXT, parse_mode=ParseMode.HTML)

app.run()