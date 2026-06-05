import asyncio
import logging
from pyrogram import Client, filters
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "business_session",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    phone_number=os.getenv("PHONE")
)


@app.on_message(filters.private & ~filters.me)
async def auto_reply(client, message):
    text = message.text.lower().strip()
    
    if "привет" in text:
        user_name = message.from_user.first_name or "User"
        await message.reply(f"Привет, {user_name}!")


async def main():
    logger.info("Bot started in Business mode")
    await app.start()
    await app.idle()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())