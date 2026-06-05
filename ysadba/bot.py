import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class QuestStates(StatesGroup):
    start = State()
    location_1 = State()
    location_1_q1 = State()
    location_1_q2 = State()
    location_1_q3 = State()
    location_1_q4 = State()
    location_2 = State()
    location_2_q1 = State()
    location_2_q2 = State()
    location_3 = State()
    location_3_q1 = State()
    location_3_q2 = State()
    location_4 = State()
    location_4_q1 = State()
    location_5 = State()
    location_5_q1 = State()
    location_6 = State()
    location_6_q1 = State()
    finished = State()


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    photo = FSInputFile("start.jpg")
    voice = FSInputFile("start.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить ➡️", callback_data="continue_to_loc1")]
    ])
    await message.answer_photo(photo=photo)
    await message.answer_voice(voice=voice, caption="Добро пожаловать в Вердомическую усадьбу графа Толочко!", reply_markup=keyboard)
    await state.set_state(QuestStates.start)


@dp.callback_query(F.data == "continue_to_loc1")
async def location_1_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    photo = FSInputFile("loca_1.jpg")
    voice = FSInputFile("loca_1.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти вопросы 📝", callback_data="loc1_questions")]
    ])
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer_voice(voice=voice, caption="Локация №1: Дворец", reply_markup=keyboard)
    await state.set_state(QuestStates.location_1)


@dp.callback_query(F.data == "loc1_questions")
async def location_1_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 1903", callback_data="loc1_q1_a")],
        [InlineKeyboardButton(text="Б) 1905", callback_data="loc1_q1_b")],
        [InlineKeyboardButton(text="В) 1907", callback_data="loc1_q1_v")]
    ])
    await callback.message.answer(
        "Вопрос 1/4:\n\nВ каком году была проведена последняя масштабная реконструкция дворца, превратившая его в роскошную резиденцию?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_1_q1)


@dp.callback_query(F.data.startswith("loc1_q1_"))
async def location_1_answer_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) 1905", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 109", callback_data="loc1_q2_a")],
        [InlineKeyboardButton(text="Б) 86", callback_data="loc1_q2_b")],
        [InlineKeyboardButton(text="В) 99", callback_data="loc1_q2_v")]
    ])
    await callback.message.answer(
        "Вопрос 2/4:\n\nСколько комнат насчитывалось во дворце в период его расцвета?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_1_q2)


@dp.callback_query(F.data.startswith("loc1_q2_"))
async def location_1_answer_2(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "v":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: В) 99", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 1915", callback_data="loc1_q3_a")],
        [InlineKeyboardButton(text="Б) 1917", callback_data="loc1_q3_b")]
    ])
    await callback.message.answer(
        "Вопрос 3/4:\n\nВ каком году во время Первой мировой войны сгорел дворец?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_1_q3)


@dp.callback_query(F.data.startswith("loc1_q3_"))
async def location_1_answer_3(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "a":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: А) 1915", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) Готика", callback_data="loc1_q4_a")],
        [InlineKeyboardButton(text="Б) Классицизм", callback_data="loc1_q4_b")],
        [InlineKeyboardButton(text="В) Барокко", callback_data="loc1_q4_v")]
    ])
    await callback.message.answer(
        "Вопрос 4/4:\n\nКакой архитектурный стиль был основой для первой каменной усадьбы, построенной в 1830 году?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_1_q4)


@dp.callback_query(F.data.startswith("loc1_q4_"))
async def location_1_answer_4(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) Классицизм", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая локация ➡️", callback_data="continue_to_loc2")]
    ])
    await callback.message.answer("Отлично! Вы завершили вопросы по локации №1.", reply_markup=keyboard)


@dp.callback_query(F.data == "continue_to_loc2")
async def location_2_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    photo = FSInputFile("loca_2.jpg")
    voice = FSInputFile("loca_2.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти вопросы 📝", callback_data="loc2_questions")]
    ])
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer_voice(voice=voice, caption="Локация №2: Липовая аллея", reply_markup=keyboard)
    await state.set_state(QuestStates.location_2)


@dp.callback_query(F.data == "loc2_questions")
async def location_2_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='А) "Тёмная улица"', callback_data="loc2_q1_a")],
        [InlineKeyboardButton(text='Б) "Тёмная аллея"', callback_data="loc2_q1_b")],
        [InlineKeyboardButton(text='В) "Мрачный лес"', callback_data="loc2_q1_v")]
    ])
    await callback.message.answer(
        "Вопрос 1/2:\n\nКакое название получила липовая аллея из-за плотно сомкнувшихся крон деревьев?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_2_q1)


@dp.callback_query(F.data.startswith("loc2_q1_"))
async def location_2_answer_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "a":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer('❌ Неправильно. Правильный ответ: А) "Тёмная улица"', show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 23 метра", callback_data="loc2_q2_a")],
        [InlineKeyboardButton(text="Б) 30 метров", callback_data="loc2_q2_b")],
        [InlineKeyboardButton(text="В) 38 метров", callback_data="loc2_q2_v")]
    ])
    await callback.message.answer(
        "Вопрос 2/2:\n\nКаких размеров достигают липы в Вердомичской аллее?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_2_q2)


@dp.callback_query(F.data.startswith("loc2_q2_"))
async def location_2_answer_2(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) 30 метров", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая локация ➡️", callback_data="continue_to_loc3")]
    ])
    await callback.message.answer("Отлично! Вы завершили вопросы по локации №2.", reply_markup=keyboard)


@dp.callback_query(F.data == "continue_to_loc3")
async def location_3_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    photo = FSInputFile("loca_3.jpg")
    voice = FSInputFile("loca_3.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти вопросы 📝", callback_data="loc3_questions")]
    ])
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer_voice(voice=voice, caption="Локация №3: Усыпальница (часовня)", reply_markup=keyboard)
    await state.set_state(QuestStates.location_3)


@dp.callback_query(F.data == "loc3_questions")
async def location_3_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) Классицизм", callback_data="loc3_q1_a")],
        [InlineKeyboardButton(text="Б) Неоготический", callback_data="loc3_q1_b")],
        [InlineKeyboardButton(text="В) Готика", callback_data="loc3_q1_v")]
    ])
    await callback.message.answer(
        "Вопрос 1/2:\n\nВ каком архитектурном стиле построена родовая часовня-усыпальница?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_3_q1)


@dp.callback_query(F.data.startswith("loc3_q1_"))
async def location_3_answer_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) Неоготический", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) Жене", callback_data="loc3_q2_a")],
        [InlineKeyboardButton(text="Б) Сыну", callback_data="loc3_q2_b")],
        [InlineKeyboardButton(text="В) Маме", callback_data="loc3_q2_v")]
    ])
    await callback.message.answer(
        "Вопрос 2/2:\n\nКому посвящена часовня?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_3_q2)


@dp.callback_query(F.data.startswith("loc3_q2_"))
async def location_3_answer_2(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) Сыну", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая локация ➡️", callback_data="continue_to_loc4")]
    ])
    await callback.message.answer("Отлично! Вы завершили вопросы по локации №3.", reply_markup=keyboard)


@dp.callback_query(F.data == "continue_to_loc4")
async def location_4_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    photo = FSInputFile("loca_4.jpg")
    voice = FSInputFile("loca_4.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти вопросы 📝", callback_data="loc4_questions")]
    ])
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer_voice(voice=voice, caption="Локация №4: Здание спиртзавода (пивоварня / бровар)", reply_markup=keyboard)
    await state.set_state(QuestStates.location_4)


@dp.callback_query(F.data == "loc4_questions")
async def location_4_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 1827", callback_data="loc4_q1_a")],
        [InlineKeyboardButton(text="Б) 1840", callback_data="loc4_q1_b")],
        [InlineKeyboardButton(text="В) 1854", callback_data="loc4_q1_v")]
    ])
    await callback.message.answer(
        "Вопрос 1/1:\n\nВ каком году был основан спиртзавод в Вердомичах?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_4_q1)


@dp.callback_query(F.data.startswith("loc4_q1_"))
async def location_4_answer_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) 1840", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая локация ➡️", callback_data="continue_to_loc5")]
    ])
    await callback.message.answer("Отлично! Вы завершили вопросы по локации №4.", reply_markup=keyboard)


@dp.callback_query(F.data == "continue_to_loc5")
async def location_5_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    photo = FSInputFile("loca_5.jpg")
    voice = FSInputFile("loca_5.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти вопросы 📝", callback_data="loc5_questions")]
    ])
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer_voice(voice=voice, caption="Локация №5: Амбар и другие хозяйственные постройки", reply_markup=keyboard)
    await state.set_state(QuestStates.location_5)


@dp.callback_query(F.data == "loc5_questions")
async def location_5_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 26 x 10 метров", callback_data="loc5_q1_a")],
        [InlineKeyboardButton(text="Б) 35 x 13 метров", callback_data="loc5_q1_b")],
        [InlineKeyboardButton(text="В) 22 x 18 метров", callback_data="loc5_q1_v")]
    ])
    await callback.message.answer(
        "Вопрос 1/1:\n\nКакие размеры имеет амбар?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_5_q1)


@dp.callback_query(F.data.startswith("loc5_q1_"))
async def location_5_answer_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "a":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: А) 26 x 10 метров", show_alert=True)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая локация ➡️", callback_data="continue_to_loc6")]
    ])
    await callback.message.answer("Отлично! Вы завершили вопросы по локации №5.", reply_markup=keyboard)


@dp.callback_query(F.data == "continue_to_loc6")
async def location_6_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    photo = FSInputFile("loca_6.jpg")
    voice = FSInputFile("loca_6.m4a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти вопросы 📝", callback_data="loc6_questions")]
    ])
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer_voice(voice=voice, caption="Локация №6: Парк и водная система", reply_markup=keyboard)
    await state.set_state(QuestStates.location_6)


@dp.callback_query(F.data == "loc6_questions")
async def location_6_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="А) 4 гектара", callback_data="loc6_q1_a")],
        [InlineKeyboardButton(text="Б) 1 гектара", callback_data="loc6_q1_b")],
        [InlineKeyboardButton(text="В) 2,5 гектара", callback_data="loc6_q1_v")]
    ])
    await callback.message.answer(
        "Вопрос 1/1:\n\nКакова общая площадь усадебного парка?",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.location_6_q1)


@dp.callback_query(F.data.startswith("loc6_q1_"))
async def location_6_answer_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    if answer == "b":
        await callback.answer("✅ Правильно!", show_alert=True)
    else:
        await callback.answer("❌ Неправильно. Правильный ответ: Б) 1 гектаров", show_alert=True)

    await callback.message.answer(
        "🎉 Поздравляем! 🎉\n\n"
        "Вы успешно прошли весь квест по Вердомической усадьбе графа Толочко!\n\n"
        "Спасибо за участие и интерес к истории этого удивительного места. "
        "Надеемся, что вы узнали много нового и интересного!\n\n"
        "Чтобы начать заново, используйте команду /start\n\n"
        "Бот создан и поддерживается @kwiken_lab"
    )
    await state.set_state(QuestStates.finished)


async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
