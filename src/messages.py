from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from constants import ALLOWED_USER_IDS
from instructions import (
    check_schedule_button_text,
    bot_info_text,
    info_button_text,
    start_message_text,
)
from kb import build_week_kb, build_main_kb

import logging

logger = logging.getLogger(name="Messages logger")

router = Router()


@router.message(F.text == check_schedule_button_text)
async def show_week(message: Message) -> None:
    week_kb = build_week_kb()
    await message.answer(text="Выберите день", reply_markup=week_kb)


@router.message(CommandStart())
async def start(message: Message) -> None:
    if str(message.from_user.id) in ALLOWED_USER_IDS:
        main_kb = build_main_kb()
        await message.answer(
            start_message_text,
            reply_markup=main_kb,
        )
    else:
        logger.warning("Unknown user, accsess denied: ", message.from_user.id)
        await message.answer(
            f"Вашего id нету в списке разрешенных id для доступа к боту, попросите добавить владельца ваш id:\n{message.from_user.id}"
        )


@router.message(F.text == info_button_text)
async def print_info(message: Message) -> None:
    await message.answer(text=bot_info_text)
