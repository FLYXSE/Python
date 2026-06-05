import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LAST_MSG_FILE = Path("last_message.json")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    name = State()
    grade = State()
    topic = State()
    subtopics = State()
    additional = State()


TOPICS = {
    "personal": {
        "title": "Личные беспокойства",
        "subtopics": [
            "Стресс", "Тревожность", "Паника", "Неуверенность", "Самокритичность",
            "Вина", "Стыд", "Пустота внутри", "Потеря опоры", "Эмоциональная усталость",
            "Напряжение", "Раздражительность", "Упадок сил", "Перегруз чувств",
            "Отключённость", "Внутренний конфликт", "Замкнутость", "Тревожные мысли",
            "Сложности с отдыхом", "Не знаю чего хочу"
        ]
    },
    "relations": {
        "title": "Проблемы в отношениях",
        "subtopics": [
            "Охлаждение", "Дистанция", "Ревность", "Недоверие", "Обиды",
            "Токсичность", "Разногласия", "Навязчивость", "Чувство одиночества в паре",
            "Эмоциональное напряжение", "Зависимость", "Отстранённость", "Конфликты",
            "Тупик", "Недопонимание"
        ]
    },
    "study": {
        "title": "Трудности в учёбе",
        "subtopics": [
            "Выгорание", "Перегруз", "Давление", "Страх ошибок", "Потеря мотивации",
            "Низкая концентрация", "Усталость", "Конфликты с одноклассниками",
            "Трудная адаптация", "Завышенные требования", "Несправедливые отметки"
        ]
    },
    "life": {
        "title": "Сложные ситуации в жизни",
        "subtopics": [
            "Болезни близких", "Трудные решения", "Переживания", "Жизненный тупик",
            "Переутомление", "Давление обстоятельств", "Угасание интереса",
            "Смена окружения", "Перемены", "Одиночество", "Неопределённость",
            "Страх будущего", "Переезд"
        ]
    },
    "home": {
        "title": "Трудности дома",
        "subtopics": [
            "Ссоры с родителями", "Непонимание в семье", "Сравнение с другими",
            "Отсутствие поддержки", "Давление требованиями", "Чувство вины",
            "Нехватка личного пространства", "Финансовые трудности семьи",
            "Развод родителей", "Болезнь члена семьи", "Неудовлетворённость домом",
            "Одиночество дома", "Напряжённая атмосфера"
        ]
    }
}


TOPIC_KEYS = list(TOPICS.keys())
SUBTOPIC_MAP = {}
SUBTOPIC_START = {}
counter = 0
for topic_idx, (topic_key, topic_data) in enumerate(TOPICS.items()):
    SUBTOPIC_START[topic_idx] = counter
    for sub in topic_data["subtopics"]:
        SUBTOPIC_MAP[counter] = (topic_idx, sub)
        counter += 1


def load_users():
    if LAST_MSG_FILE.exists():
        with open(LAST_MSG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(data):
    with open(LAST_MSG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def can_send_message(user_id: int) -> tuple[bool, str]:
    users = load_users()
    user_data = users.get(str(user_id))

    if user_data and user_data.get("last_time"):
        last_time = datetime.fromisoformat(user_data["last_time"])
        next_time = last_time + timedelta(hours=12)
        if datetime.now() < next_time:
            remaining = next_time - datetime.now()
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            return False, f"{hours} часов {minutes} минут"

    return True, ""


def save_last_message_time(user_id: int, username: str):
    users = load_users()
    users[str(user_id)] = {
        "id": user_id,
        "username": username,
        "last_time": datetime.now().isoformat()
    }
    save_users(users)


def build_topic_keyboard():
    keyboard = []
    for idx, (key, data) in enumerate(TOPICS.items()):
        keyboard.append([InlineKeyboardButton(text=data["title"], callback_data=f"TOPIC:{idx}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def build_subtopics_keyboard(selected: list[int], topic_idx: int):
    keyboard = []
    topic_key = TOPIC_KEYS[topic_idx]
    topic_data = TOPICS[topic_key]

    for idx, sub in enumerate(topic_data["subtopics"]):
        global_idx = SUBTOPIC_START[topic_idx] + idx
        marker = "✅ " if global_idx in selected else ""
        keyboard.append([InlineKeyboardButton(text=f"{marker}{sub}", callback_data=f"SUB:{global_idx}")])

    keyboard.append([
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_topics"),
        InlineKeyboardButton(text="Продолжить ▶️", callback_data=f"CONT:{topic_idx}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    can_send, remaining = can_send_message(message.from_user.id)

    if not can_send:
        await message.answer(
            f"⏳ Подожди, ты уже отправлял сообщение.\n"
            f"Повторно можно написать через {remaining}.\n\n"
            "Если тебе нужна срочная помощь - позвони на горячую линию:\n📞 133\n📞 8(0152) 67 76 21"
        )
        return

    await message.answer(
        "Привет! 👋 Я бот психологической поддержки для школьников.\n\n"
        "Здесь ты можешь поделиться своими переживаниями, и наши психологи помогут тебе справиться с трудностями.\n\n"
        "Это бесплатная помощь, и всё, что ты напишешь - конфиденциально.\n\n"
        "Чтобы начать, введи своё имя и фамилию:"
    )
    await state.set_state(Form.name)


@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введи класс (параллель и букву), например: 9А")
    user_id = message.from_user.id or "не указан"
    username = message.from_user.username or "не указан"
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def get_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer(
        "📋 Выбери тему для обсуждения:",
        reply_markup=build_topic_keyboard()
    )
    await state.set_state(Form.topic)


@dp.callback_query(F.data.startswith("TOPIC:"))
async def select_topic(callback, state: FSMContext):
    topic_idx = int(callback.data.split(":")[1])
    await state.update_data(topic_idx=topic_idx, selected_subtopics=[])
    topic_key = TOPIC_KEYS[topic_idx]
    await callback.message.edit_text(
        f"📌 Тема: {TOPICS[topic_key]['title']}\n\nВыбери то, что тебя беспокоит:",
        reply_markup=build_subtopics_keyboard([], topic_idx)
    )


@dp.callback_query(F.data.startswith("SUB:"))
async def toggle_subtopic(callback, state: FSMContext):
    global_idx = int(callback.data.split(":")[1])
    topic_idx, subtopic = SUBTOPIC_MAP[global_idx]

    data = await state.get_data()
    selected = data.get("selected_subtopics", [])

    if global_idx in selected:
        selected.remove(global_idx)
    else:
        selected.append(global_idx)

    await state.update_data(selected_subtopics=selected)
    topic_key = TOPIC_KEYS[topic_idx]
    await callback.message.edit_text(
        f"📌 Тема: {TOPICS[topic_key]['title']}\n\nВыбери то, что тебя беспокоит:",
        reply_markup=build_subtopics_keyboard(selected, topic_idx)
    )


@dp.callback_query(F.data == "back_to_topics")
async def back_to_topics(callback, state: FSMContext):
    await callback.message.edit_text(
        "📋 Выбери тему для обсуждения:",
        reply_markup=build_topic_keyboard()
    )
    await state.set_state(Form.topic)


@dp.callback_query(F.data.startswith("CONT:"))
async def continue_to_additional(callback, state: FSMContext):
    topic_idx = int(callback.data.split(":")[1])
    data = await state.get_data()
    selected = data.get("selected_subtopics", [])

    topic_key = TOPIC_KEYS[topic_idx]
    selected_subtopics = [SUBTOPIC_MAP[idx][1] for idx in selected]

    await state.update_data(
        topic_idx=topic_idx,
        topic_title=TOPICS[topic_key]["title"],
        subtopics=selected_subtopics
    )

    subtopics_text = ", ".join(selected_subtopics) if selected_subtopics else "не выбраны"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить описание ✏️", callback_data="add_text")],
        [InlineKeyboardButton(text="Отправить без описания 🚀", callback_data="send_now")]
    ])

    await callback.message.edit_text(
        f"📝 Тема: {TOPICS[topic_key]['title']}\n\n"
        f"🏷️ Подтемы: {subtopics_text}\n\n"
        f"Хочешь добавить что-то ещё своими словами?",
        reply_markup=keyboard
    )
    await state.set_state(Form.additional)


@dp.callback_query(F.data == "add_text")
async def ask_for_text(callback, state: FSMContext):
    await callback.message.edit_text(
        "Напиши своими словами, что тебя беспокоит:\n\n"
        "(Нажми /skip чтобы пропустить)"
    )


@dp.callback_query(F.data == "send_now")
async def send_without_text(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["user_id"] = callback.from_user.id
    data["username"] = callback.from_user.username

    await callback.message.edit_text(
        callback.message.text,
        reply_markup=None
    )

    await finalize(callback.message, state, data, "")


@dp.message(Form.additional, F.text == "/skip")
async def skip_text(message: Message, state: FSMContext):
    await send_message_from_state(message, state, "")


@dp.message(Form.additional)
async def receive_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await finalize(message, state, data, message.text)


async def finalize(message: Message, state: FSMContext, data: dict, text: str):
    user_id = data.get("user_id") or message.from_user.id
    username = data.get("username") or message.from_user.username or "не указан"
    name = data.get("name") or "не указано"
    grade = data.get("grade") or "не указан"
    topic = data.get("topic_title", "")
    subtopics = data.get("subtopics", [])
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")

    subtopics_text = ", ".join(subtopics) if subtopics else "не указаны"
    full_message = f"{text}" if text else "без описания"

    message_for_chat = (
        f"📩 Новое обращение:\n\n"
        f"👤 Имя: {name}\n"
        f"📚 Класс: {grade}\n"
        f"🔗 Telegram: @{username}\n"
        f"🆔 ID: {user_id}\n"
        f"🕐 Время: {timestamp}\n\n"
        f"📋 Тема: {topic}\n"
        f"🏷️ Подтемы: {subtopics_text}\n\n"
        f"💬 Сообщение:\n{full_message}"
    )

    if CHAT_ID:
        await bot.send_message(CHAT_ID, message_for_chat)

    save_last_message_time(user_id, username)

    await message.answer(
        "✅ Спасибо! Твоё сообщение отправлено.\n\n"
        "Наши психологи свяжутся с тобой в ближайшее время. Не переживай - ты не один! 💙"
    )
    await state.clear()


async def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set")
        return
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())