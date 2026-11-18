from datetime import datetime

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
)

from callback_structs import Homework, LessonCb
from constants import DAYS
from kb import build_days_kb, build_lesson_keyboard, build_schedule_keyboard
from server import ScheduleUnavailableError, get_data, get_homework, get_subject_name

router = Router()


@router.callback_query(F.data == "back_to_week")
async def back_to_week(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите день недели:", reply_markup=build_days_kb()
    )
    await callback.answer()


@router.callback_query(Homework.filter(F.action == "back_to_lessons"))
async def back_to_lessons(callback: CallbackQuery, callback_data: Homework):
    try:
        kb = await build_schedule_keyboard(callback_data.day)
    except ScheduleUnavailableError:
        await callback.message.message(
            "Не удалось получить расписание на день. Попробуйте позже.",
            show_alert=True,
        )
        return
    day = datetime.fromisoformat(callback_data.day).weekday()
    await callback.message.edit_text(
        text=f"Расписание на день: {DAYS[day]}", reply_markup=kb
    )
    await callback.answer()


@router.callback_query(LessonCb.filter(F.action == "show"))
async def show_day_schedule(callback: CallbackQuery, callback_data: LessonCb):
    await callback.answer()
    try:
        kb = await build_schedule_keyboard(callback_data.day)
    except ScheduleUnavailableError:
        await callback.message.answer(
            "Не удалось получить расписание на день. Попробуйте позже.",
            show_alert=True,
        )
        return
    day = datetime.fromisoformat(callback_data.day).weekday()
    await callback.message.edit_text(
        f"Расписание на день: {DAYS[day]}", reply_markup=kb
    )


@router.callback_query(Homework.filter(F.action == "homework"))
async def show_homework(callback: CallbackQuery, callback_data: Homework):
    await callback.answer()
    try:
        try:
            data = await get_data(callback_data.day)
        except ScheduleUnavailableError:
            await callback.message.answer(
                text=f"Не удалось получить данные о дне. Попробуйте позже."
            )
            return
        subject_name = await get_subject_name(callback_data, data)
        homework = await get_homework(callback_data, data)
        await callback.message.edit_text(
            text=f"Домашняя работа по: {subject_name}\n{homework}",
            reply_markup=build_lesson_keyboard(callback_data),
        )
    except Exception:
        await callback.message.answer(
            text="Не удалось получить данные о домашней работе. Пожалуйста, попробуйте позже.",
        )


@router.callback_query(F.data == "close")
async def close(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
