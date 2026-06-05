import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from services.routing import build_map

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
USE_GOOGLE = True

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

PLACES = {
    "old_castle": {
        "name": "🏰 Старый замок",
        "lat": 53.6784,
        "lon": 23.8295,
        "videos": [("YouTube", "https://www.youtube.com/watch?v=VIDEO_ID&t=120s")]
    },
    "new_castle": {
        "name": "🏯 Новый замок",
        "lat": 53.6789,
        "lon": 23.8302,
        "videos": [("VK", "https://vk.com/video-123456?t=90")]
    }
}

# временно сохраняем локацию пользователя
USER_LOCATIONS = {}

@dp.message(CommandStart())
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Отправить локацию", request_location=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Я покажу тебе достопримечательности Гродно 🚶‍♂️\n"
        "Отправь свою локацию.",
        reply_markup=kb
    )

@dp.message(F.location)
async def handle_location(message: Message):
    user_lat = message.location.latitude
    user_lon = message.location.longitude
    USER_LOCATIONS[message.from_user.id] = (user_lat, user_lon)

    places_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=place["name"], callback_data=key)]
            for key, place in PLACES.items()
        ]
    )

    # карта текущей локации без маршрута
    map_url = build_map((user_lat, user_lon), (user_lat, user_lon))

    await message.answer_photo(
        photo=map_url,
        caption="📍 Ты здесь. Выбери место рядом:",
        reply_markup=places_kb
    )

@dp.callback_query()
async def place_selected(call):
    place = PLACES[call.data]
    user_loc = USER_LOCATIONS.get(call.from_user.id)

    if not user_loc:
        await call.message.answer("Сначала отправь свою локацию 📍")
        return

    # строим маршрут от пользователя до места
    route_url = build_map(user_loc, (place['lat'], place['lon']))

    videos = "\n".join(f"▶ {name}: {url}" for name, url in place["videos"])
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Вернуться к карте", callback_data="back")]]
    )

    await call.message.answer_photo(
        photo=route_url,
        caption=f"📍 {place['name']}\n\n🎥 Видео:\n{videos}",
        reply_markup=kb
    )

@dp.callback_query(F.data == "back")
async def back_to_map(call):
    await call.message.answer("Отправь локацию ещё раз 📍")

if __name__ == "__main__":
    dp.run_polling(bot)
