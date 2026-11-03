from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart

from utils import get_week_list
from callback_structs import LessonCb
from kb import build_main_kb, build_days_kb
from instructions import info, watch_for_weekdays_button, info_button, start_message

router = Router()


@router.message(F.text == watch_for_weekdays_button)
async def show_schedule(message: Message):
    await message.answer(text="Выберите день", reply_markup=build_days_kb())


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        start_message,
        reply_markup=build_main_kb(),
    )


@router.message(F.text == info_button)
async def print_info(message: Message):
    await message.answer(text=info)
