import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ButtonStyle
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# ===================== НАСТРОЙКИ =====================
logging.basicConfig(level=logging.INFO)

API_TOKEN = "8039100996:AAEJuAgGh4b6Vnq1YXIxn0Zu79IeZoG1pj8"

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ===================== FSM =====================
class TourStates(StatesGroup):
    waiting_start = State()
    dvorec_questions = State()
    dvorec_q1 = State()
    dvorec_q2 = State()
    dvorec_q3 = State()
    dvorec_q4 = State()
    lipa_wait = State()
    lipa_questions = State()

# ===================== КЛАВИАТУРЫ =====================
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡️ Начать ⚡️", callback_data="start", style=ButtonStyle.SUCCESS)]
    ])


def questions_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓ Вопросы ❓", callback_data="show_questions", style=ButtonStyle.SUCCESS)]
    ])


def next_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Дальше ➡️", callback_data="next_location", style=ButtonStyle.SUCCESS)]
    ])


# ===================== ХЭНДЛЕРЫ =====================

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(TourStates.waiting_start)
    
    audio = FSInputFile("start.m4a")
    
    await message.answer_voice(
        voice=audio,
        caption="<b>Добро пожаловать!</b>\n\n",
        reply_markup=start_kb()
    )


@dp.callback_query(F.data == "start")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    audio = FSInputFile("dvorec.m4a")
    
    await callback.message.answer_voice(
        voice=audio,
        caption="<b>Дворец</b>",
        reply_markup=questions_kb()
    )
    
    await state.set_state(TourStates.dvorec_questions)


@dp.callback_query(F.data == "show_questions", StateFilter(TourStates.dvorec_questions))
async def dvorec_questions(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.answer(
        "1) В каком году была проведена последняя масштабная реконструкция дворца, "
        "превратившая его в роскошную резиденцию?\n\n"
        "<b>Варианты:</b>\n"
        "А: 1900\n"
        "Б: 1913\n"
        "В: 1905\n"
    )
    await state.set_state(TourStates.dvorec_q1)


@dp.message(StateFilter(TourStates.dvorec_q1))
async def dvorec_q1_answer(message: Message, state: FSMContext):
    if message.text.strip() in ["В", "в"]:
        await message.answer("<b>✅ Правильно!</b>")
        
        await message.answer(
            "2) Сколько комнат насчитывалось во дворце в период его расцвета?\n\n"
            "<b>Варианты:</b>\n"
            "А: 99\n"
            "Б: 83\n"
            "В: 101\n"
            )
        await state.set_state(TourStates.dvorec_q2)
        
    else:
        await message.answer("❌ Неправильно. Попробуйте ещё раз.")


@dp.message(StateFilter(TourStates.dvorec_q2))
async def dvorec_q2_answer(message: Message, state: FSMContext):
    if message.text.strip() in ["А", "а"]:
        await message.answer("<b>✅ Правильно!</b>")
        
        await message.answer(
            "3) Когда и при каких обстоятельствах был утрачен дворец?\n\n"
            "<b>Варианты:</b>\n"
            "А:\n"
            "Б: Сгорел в 1915 году.\n"
            "В:\n"
            )
        await state.set_state(TourStates.dvorec_q3)
    else:
        await message.answer("❌ Неправильно. Попробуйте ещё раз.")


@dp.message(StateFilter(TourStates.dvorec_q3))
async def dvorec_q3_answer(message: Message, state: FSMContext):
    if message.text.strip() in ["Б", "б"]:
        await message.answer("<b>✅ Правильно!</b>")
        
        await message.answer(
            "4) Какой архитектурный стиль был основной для первой каменой усадьбы, потороенной в 1830 году?\n\n"
            "<b>Варианты:</b>\n"
            "А: Готика\n"
            "Б: Классицизм\n"
            "В: Романский\n"
        )
        await state.set_state(TourStates.dvorec_q4)
    else:
        await message.answer("❌ Неправильно. Попробуйте ещё раз.")
        

@dp.message(StateFilter(TourStates.dvorec_q4))
async def dvorec_q4_answer(message: Message, state: FSMContext):
    if message.text.strip() in ["Б", "б"]:
        await message.answer("<b>✅ Правильно!</b>")
        
        
        await message.answer("Дворец пройден!",
                             reply_markup=next_kb())

        await state.set_state(TourStates.lipa_wait)
    else:
        await message.answer("❌ Неправильно. Попробуйте ещё раз.")

# ===================== Липовая аллея =====================
@dp.callback_query(F.data == "next_location", StateFilter("TourStates.lipa_wait"))
async def lipa(callback: CallbackQuery, state: FSMContext):
   
        audio = FSInputFile("lipa.m4a")
    
        await callback.message.answer_voice(
            voice=audio,
            caption="<b>Липовая аллея</b>",
            reply_markup=show_questions()
        )
    
        await state.set_state(TourStates.lipa_questions)


@dp.callback_query(F.data == "show_questions", StateFilter(TourStates.lipa_questions))
async def lipa_questions(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.answer(
        "1) Какое название получила липовая аллея из-за плотно сомкнувшихся крон деревьев?\n\n"
        "<b>Варианты</b>\n"
        "А: Темная улица"
        "Б: Мрачная аллея"
        "В: Чёрный лес",
        reply_markup=None
    )
    
    await state.set_state(TourStates.lipa_q1)


@dp.message(StateFilter(TourStates.lipa_q1))
async def lipa_q1(message: Message, state: FSMContext):
    if message.text.strip() in ["А", "а"]:
        await message.answer(
            "<b>✅ Правильно!</b>")
        await message.answer(
            "2) Какихразмеров достигают липы в Вердомической аллее?\n\n"
            "<b>Варианты</b>\n"
            "А: 20"
            "Б: 33"
            "В: 30"
        )
        await state.set_state(TourStates.lipa_q2)
    else:
        await message.answer("❌ Неправильно. Попробуйте ещё раз.")
        

@dp.message(StateFilter(TourStates.lipa_q2))
async def lipa_q2(message: Message, state: FSMContext):
    if message.text.strip() in ["В", "в"]:
        await message.answer(
            "<b>✅ Правильно!</b>")
        await message.answer(
            "3) Какие редкие породы деревьев, встречаются в парке усадьбы\n\n"
            "<b>Варианты</b>\n"
            "А: True"
            "Б: False"
            "В: False"
        )
        await state.set_state(TourStates.ysip_wait)
    else:
        await message.answer("❌ Неправильно. Попробуйте ещё раз.")


@dp.callback_query(F.data == "next_location", StateFilter("TourStates.ysip_wait"))
async def ysip(callback: CallbackQuery, state: FSMContext):
   
        audio = FSInputFile("ysip.m4a")
    
        await callback.message.answer_voice(
            voice=audio,
            caption="<b>Усыпальница (часовня)</b>",
            reply_markup=show_questions()
        )
    
        await state.set_state(TourStates.ysip_)

# ===================== ЗАПУСК =====================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())