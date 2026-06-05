from pyrogram import Client, filters
from pyrogram.types import Message
from texts import *
from emoji import *
import asyncio
import re


async def clear(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit(LSD_clear_me)
        return

    arg = message.command[1].lower().strip()

    if arg not in ["+me", "+all"]:
        await message.edit(LSD_clear_me)
        return

    wait_msg = await message.edit(LSD_clear_wait)

    # Ожидаем ответ в этом же чате от себя
    try:
        response = await client.listen(
            filters.chat(message.chat.id) &
            filters.me &
            filters.regex(r"^LSD\.clear\.(YES|NO)$", flags=re.IGNORECASE),
            timeout=60
        )
    except asyncio.TimeoutError:
        await wait_msg.delete()
        return
    except Exception:
        await wait_msg.delete()
        return

    resp_text = response.text.upper() if response.text else ""

    if "NO" in resp_text:
        await asyncio.sleep(0.3)
        await wait_msg.delete()
        await response.delete()
        return

    # YES подтверждено
    await wait_msg.delete()
    await response.delete()

    if arg == "+me":
        try:
            async for msg in client.get_chat_history(message.chat.id, limit=1500):
                if msg.from_user and msg.from_user.is_self and not msg.empty:
                    try:
                        await msg.delete()
                        await asyncio.sleep(0.12)
                    except:
                        pass
            await client.send_message(
                message.chat.id,
                LSD_clear_me,
                disable_notification=True
            )
        except Exception:
            pass

    elif arg == "+all":
        try:
            async for msg in client.get_chat_history(message.chat.id, limit=1500):
                if not msg.empty:
                    try:
                        await msg.delete()
                        await asyncio.sleep(0.12)
                    except:
                        pass
            await client.send_message(
                message.chat.id,
                LSD_clear_all,
                disable_notification=True
            )
        except Exception:
            pass