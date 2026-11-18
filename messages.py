from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from constants import OWNER_ID
from instructions import info, info_button, start_message, watch_for_weekdays_button
from kb import build_days_kb, build_main_kb

router = Router()


@router.message(F.text == watch_for_weekdays_button)
async def show_schedule(message: Message):
    await message.answer(text="Выберите день", reply_markup=build_days_kb())


@router.message(CommandStart())
async def start(message: Message):
    if message.from_user.id in OWNER_ID:
        await message.answer(
            start_message,
            reply_markup=build_main_kb(),
        )
    else:
        await message.answer(
            f"Вашего id нету в списке разрешенных id для доступа к боту, попросите добавить владельца ваш id:\n{message.from_user.id}"
        )


@router.message(F.text == info_button)
async def print_info(message: Message):
    await message.answer(text=info)
