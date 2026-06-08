import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
CRYPTOPAY_TOKEN: str = os.getenv("CRYPTOPAY_TOKEN", "")
CRYPTOPAY_URL: str = os.getenv("CRYPTOPAY_URL", "http://cryptoplaggy.ru:15048/api/v1/")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in .env")
if not CRYPTOPAY_TOKEN:
    raise ValueError("CRYPTOPAY_TOKEN not set in .env")
