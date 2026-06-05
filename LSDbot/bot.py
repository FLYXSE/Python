import asyncio
import logging
import random
import sqlite3
import os
from datetime import datetime

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import cloudinary
import cloudinary.api
from groq import Groq

# ────────────────────────────────────────────────
#                  НАСТРОЙКИ
# ────────────────────────────────────────────────

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_USER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("bot.log", encoding="utf-8"))

# SQLite
conn = sqlite3.connect("bot_data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS used_memes (public_id TEXT PRIMARY KEY)")
cur.execute("""
    CREATE TABLE IF NOT EXISTS poll_votes 
    (message_id INTEGER, user_id INTEGER, choice TEXT, PRIMARY KEY(message_id, user_id))
""")
conn.commit()

# FSM для /post
class PostForm(StatesGroup):
    text = State()
    media = State()
    buttons = State()
    confirm = State()

# Router
router = Router()
last_poll_id = None

# ────────────────────────────────────────────────
#                  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ────────────────────────────────────────────────

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


async def check_admin(message: Message) -> bool:
    if not is_admin(message.from_user.id):
        await message.answer("Доступ запрещён.")
        return False
    return True


def get_unused_memes():
    try:
        result = cloudinary.api.resources(
            resource_type="image",
            prefix="memes/",
            max_results=500
        )
        all_ids = [res["public_id"] for res in result.get("resources", [])]
        cur.execute("SELECT public_id FROM used_memes")
        used = {row[0] for row in cur.fetchall()}
        return [pid for pid in all_ids if pid not in used]
    except Exception as e:
        logger.error(f"Cloudinary ошибка: {e}")
        return []


def mark_meme_used(public_id: str):
    cur.execute("INSERT OR IGNORE INTO used_memes (public_id) VALUES (?)", (public_id,))
    conn.commit()


# ────────────────────────────────────────────────
#                  МЕМЫ
# ────────────────────────────────────────────────

async def publish_meme(bot: Bot):
    unused = get_unused_memes()
    if not unused:
        logger.warning("Не осталось неиспользованных мемов")
        return

    public_id = random.choice(unused)
    url = f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/image/upload/{public_id}"

    try:
        await bot.send_photo(CHANNEL_ID, url, caption="Test")
        mark_meme_used(public_id)
        logger.info(f"Мем опубликован: {public_id}")
    except Exception as e:
        logger.error(f"Ошибка публикации мема: {e}")


# ────────────────────────────────────────────────
#                  ЧТО БЫ ТЫ ВЫБРАЛ (Опрос)
# ────────────────────────────────────────────────

async def generate_question():
    prompt = (
        "Сгенерируй 1 смешной/провокационный вопрос в формате "
        "\"Что бы ты выбрал — [А] или [Б]?\" "
        "на тему жизни, технологий, отношений или еды. "
        "Только один вопрос, без лишнего текста."
    )
    try:
        resp = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
            temperature=0.9,
            max_tokens=120
        )
        question = resp.choices[0].message.content.strip()
        if " — " not in question:
            return "Что бы ты выбрал — миллион рублей или вечную любовь?", "миллион рублей", "вечную любовь"
        a, b_part = question.split(" — ", 1)
        b = b_part.rstrip("?")
        return question, a.strip(), b.strip()
    except Exception as e:
        logger.error(f"Groq ошибка: {e}")
        return "Что бы ты выбрал — пиццу или суши?", "пиццу", "суши"


async def publish_poll(bot: Bot):
    global last_poll_id
    question, opt_a, opt_b = await generate_question()

    text = f"{question}\n\nПервое 0 | Второе 0"
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(opt_a, callback_data=f"poll_a|{opt_a}"),
        InlineKeyboardButton(opt_b, callback_data=f"poll_b|{opt_b}")
    ]])

    msg = await bot.send_message(CHANNEL_ID, text, reply_markup=kb)
    last_poll_id = msg.message_id

    # Очищаем старые голоса
    cur.execute("DELETE FROM poll_votes WHERE message_id != ?", (last_poll_id,))
    conn.commit()
    logger.info("Опрос опубликован")


@router.callback_query(F.data.startswith("poll_"))
async def handle_vote(callback: CallbackQuery):
    global last_poll_id
    if callback.message.message_id != last_poll_id:
        return

    _, choice_str = callback.data.split("|", 1)
    choice = callback.data[5]  # a или b

    user_id = callback.from_user.id
    cur.execute(
        "INSERT OR REPLACE INTO poll_votes VALUES (?,?,?)",
        (callback.message.message_id, user_id, choice)
    )
    conn.commit()

    cur.execute(
        "SELECT choice, COUNT(*) FROM poll_votes WHERE message_id = ? GROUP BY choice",
        (callback.message.message_id,)
    )
    votes = dict(cur.fetchall())

    new_text = f"{callback.message.text.splitlines()[0]}\n\nПервое {votes.get('a', 0)} | Второе {votes.get('b', 0)}"

    try:
        await callback.message.edit_text(new_text, reply_markup=callback.message.reply_markup)
        await callback.answer("Голос засчитан!")
    except Exception:
        pass


# ────────────────────────────────────────────────
#                  ФЕЙКОВЫЕ НОВОСТИ
# ────────────────────────────────────────────────

async def generate_fake_news():
    prompt = (
        "Придумай 1 короткую сенсационную фейковую новость в стиле 2026 года, "
        "смешную и кликбейтную. Темы: IT, Telegram, крипта, программирование. "
        "Заголовок + 2–4 предложения. Только текст новости."
    )
    try:
        resp = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
            temperature=1.0,
            max_tokens=200
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq ошибка: {e}")
        return (
            "Telegram в 2026 году ввёл встроенный ИИ-майнинг TON прямо в голосовых чатах — "
            "пользователи зарабатывают $500 в день, просто болтая с друзьями!"
        )


async def publish_news(bot: Bot):
    news_text = await generate_fake_news()
    try:
        await bot.send_message(CHANNEL_ID, news_text)
        logger.info("Фейковая новость опубликована")
    except Exception as e:
        logger.error(f"Ошибка отправки новости: {e}")


# ────────────────────────────────────────────────
#                  КОМАНДЫ
# ────────────────────────────────────────────────

@router.message(Command("meme"))
async def cmd_meme(message: Message, bot: Bot):
    if not await check_admin(message):
        return
    await publish_meme(bot)
    await message.answer("Мем опубликован!")


@router.message(Command("what"))
async def cmd_what(message: Message, bot: Bot):
    if not await check_admin(message):
        return
    await publish_poll(bot)
    await message.answer("Опрос опубликован!")


@router.message(Command("news"))
async def cmd_news(message: Message, bot: Bot):
    if not await check_admin(message):
        return
    await publish_news(bot)
    await message.answer("Фейковая новость опубликована!")


# ────────────────────────────────────────────────
#                  /post (произвольный пост)
# ────────────────────────────────────────────────

@router.message(Command("post"))
async def start_post(message: Message, state: FSMContext):
    if not await check_admin(message):
        return
    await message.answer("Отправь текст поста (поддерживается HTML)")
    await state.set_state(PostForm.text)


@router.message(PostForm.text)
async def get_post_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Отправь фото, видео или GIF\nИли напиши /skip")
    await state.set_state(PostForm.media)


@router.message(PostForm.media)
async def get_media(message: Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(media=None, media_type=None)
    elif message.photo:
        await state.update_data(media=message.photo[-1].file_id, media_type="photo")
    elif message.video:
        await state.update_data(media=message.video.file_id, media_type="video")
    elif message.animation:
        await state.update_data(media=message.animation.file_id, media_type="animation")
    else:
        await message.answer("Поддерживаются только фото/видео/GIF. Повтори или /skip")
        return

    await message.answer(
        "Хочешь добавить кнопки?\n\n"
        "Формат (по одной кнопке на строку):\n"
        "Кнопка 1 - https://example.com\n"
        "Кнопка 2 - https://t.me/channel\n"
        "\nИли напиши /skip"
    )
    await state.set_state(PostForm.buttons)


@router.message(PostForm.buttons)
async def get_buttons(message: Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(buttons=None)
    else:
        lines = message.text.strip().split("\n")
        inline_kb = []
        for line in lines:
            if " - " in line:
                name, url = [x.strip() for x in line.split(" - ", 1)]
                inline_kb.append([InlineKeyboardButton(text=name, url=url)])
        if inline_kb:
            await state.update_data(buttons=InlineKeyboardMarkup(inline_keyboard=inline_kb))
        else:
            await state.update_data(buttons=None)

    data = await state.get_data()
    preview = f"Текст: {data.get('text', '')[:200]}...\n"
    preview += f"Медиа: {'есть' if data.get('media') else 'нет'}\n"
    preview += f"Кнопки: {'есть' if data.get('buttons') else 'нет'}"

    await message.answer(f"{preview}\n\nОпубликовать пост?  Да / Нет / Изменить")
    await state.set_state(PostForm.confirm)


@router.message(PostForm.confirm)
async def confirm_post(message: Message, state: FSMContext, bot: Bot):
    text = message.text.lower()
    data = await state.get_data()

    if "да" in text:
        try:
            kb = data.get("buttons")
            if data.get("media"):
                if data["media_type"] == "photo":
                    await bot.send_photo(
                        chat_id=CHANNEL_ID,
                        photo=data["media"],
                        caption=data["text"],
                        reply_markup=kb
                    )
                elif data["media_type"] == "video":
                    await bot.send_video(
                        chat_id=CHANNEL_ID,
                        video=data["media"],
                        caption=data["text"],
                        reply_markup=kb
                    )
                else:
                    await bot.send_animation(
                        chat_id=CHANNEL_ID,
                        animation=data["media"],
                        caption=data["text"],
                        reply_markup=kb
                    )
            else:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=data["text"],
                    reply_markup=kb
                )
            await message.answer("Пост успешно опубликован!")
        except Exception as e:
            logger.error(f"Ошибка публикации поста: {e}")
            await message.answer("Не удалось опубликовать пост. Проверь логи.")
    else:
        await message.answer("Публикация отменена.")

    await state.clear()


# ────────────────────────────────────────────────
#                  ЗАПУСК БОТА
# ────────────────────────────────────────────────

async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в .env")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(publish_meme,   "interval", hours=2,   args=[bot])
    scheduler.add_job(publish_poll,   "cron",    hour=19, minute=0, args=[bot])
    scheduler.add_job(publish_news,   "cron",    hour=12, minute=0, args=[bot])
    scheduler.start()

    logger.info("Бот запущен (aiogram 3.24.0)")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    asyncio.run(main())