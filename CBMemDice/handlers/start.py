from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import main_menu_kb
import database
import texts
from utils import safe_edit

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    database.get_or_create_user(
        message.from_user.id,
        message.from_user.username or "",
    )
    await message.answer(texts.START_WELCOME, reply_markup=main_menu_kb())


@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    await safe_edit(callback.message, texts.MAIN_MENU, reply_markup=main_menu_kb())
    await callback.answer()
