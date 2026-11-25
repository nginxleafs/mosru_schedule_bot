from datetime import datetime

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
)

from callback_structs import Homework, Lesson, Day
from constants import DAYS
from kb import build_week_kb, build_homework_kb, build_subjects_kb
from server import ScheduleUnavailableError, get_data, get_homework, get_subject_name

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "back_to_week")
async def back_to_week(callback: CallbackQuery) -> None:
    await callback.answer()
    week_kb = build_week_kb()
    await callback.message.edit_text(text="Выберите день недели:", reply_markup=week_kb)


@router.callback_query(Lesson.filter(F.action == "back_to_subjects"))
async def back_to_lessons(callback: CallbackQuery, callback_data: Lesson) -> None:
    await callback.answer()
    try:
        data = await get_data(requested_date_str=callback_data.date, callback=callback)
    except ScheduleUnavailableError:
        return
    kb = build_subjects_kb(data=data, date=callback_data.date)
    day = datetime.fromisoformat(callback_data.date).weekday()
    await callback.message.edit_text(
        text=f"Расписание на день: {DAYS[day]}", reply_markup=kb
    )


@router.callback_query(Day.filter(F.action == "show_subjects"))
async def show_day_schedule(callback: CallbackQuery, callback_data: Day) -> None:
    await callback.answer()
    try:
        data = await get_data(requested_date_str=callback_data.date, callback=callback)
    except ScheduleUnavailableError:
        return
    kb = build_subjects_kb(data, date=callback_data.date)
    day = datetime.fromisoformat(callback_data.date).weekday()
    await callback.message.edit_text(
        text=f"Расписание на день: {DAYS[day]}", reply_markup=kb
    )


@router.callback_query(Homework.filter(F.action == "show_subject_homework"))
async def show_homework(callback: CallbackQuery, callback_data: Homework) -> None:
    await callback.answer()
    try:
        data = await get_data(requested_date_str=callback_data.date, callback=callback)
    except ScheduleUnavailableError:
        return

    subject_name = get_subject_name(callback_data, data)
    homework = get_homework(callback_data, data)
    homework_kb = build_homework_kb(callback_data)
    await callback.message.edit_text(
        text=f"Домашняя работа по: {subject_name}\n{homework}",
        reply_markup=homework_kb,
    )


@router.callback_query(F.data == "close")
async def close(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
