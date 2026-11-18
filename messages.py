from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from instructions import info, info_button, start_message, watch_for_weekdays_button
from kb import build_days_kb, build_main_kb

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
