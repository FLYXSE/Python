import asyncio
import logging
from telethon import TelegramClient, events
import aiohttp
import os

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = "lsd_ai_session"

AI_API_KEY = "sk-9ebb09491b7d307d-ad0cc9-b6f5b6d8"
AI_API_URL = "https://omniroute.ai/v1/chat/completions"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def get_ai_response(question: str) -> str:
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(AI_API_URL, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"Ошибка API: {response.status}"

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.AI (.+)'))
async def handle_ai_question(event):
    question = event.pattern_match.group(1).strip()

    if not question:
        return

    await event.edit("🌈 **LSD AI**\n\n⏳ Думаю...")

    try:
        answer = await get_ai_response(question)
        await event.edit(f"🌈 **LSD AI**\n\n{answer}")
    except Exception as e:
        await event.edit(f"🌈 **LSD AI**\n\n❌ Ошибка: {str(e)}")

async def main():
    await client.start()
    print("✅ LSD AI userbot запущен!")
    print("Используй: .AI вопрос")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
