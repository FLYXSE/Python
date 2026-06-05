# memdice_bot/utils.py
import asyncio
from aiogram import Bot
from typing import List
import texts
import keyboards

async def check_subscription(bot: Bot, user_id: int, channels: List[str]) -> bool:
    if not channels:
        return True
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            # Если канал недоступен или ошибка — считаем не подписанным
            return False
    return True


async def ensure_subscribed(message, bot, channels):
    if await check_subscription(bot, message.from_user.id, channels):
        return True
    kb = keyboards.get_subscribe_keyboard(channels)
    await message.answer(texts.SUBSCRIBE_PROMPT, reply_markup=kb)
    return False