from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    Message,
)

from server import get_homework, get_subject_name
from constants import DAYS
from callback_structs import Homework, LessonCb
from kb import build_schedule_keyboard, build_lesson_keyboard, build_days_kb
from utils import get_week_list


router = Router()


@router.callback_query(F.data == "back_to_week")
async def back_to_week(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите день недели:", reply_markup=build_days_kb()
    )


@router.callback_query(Homework.filter(F.action == "back_to_lessons"))
async def back_to_lessons(callback: CallbackQuery, callback_data: Homework):
    kb = await build_schedule_keyboard(callback_data.day)
    week = get_week_list()
    await callback.message.edit_text(
        text=f"Расписание на день: {week[callback_data.day]}", reply_markup=kb
    )
    return True


@router.callback_query(LessonCb.filter(F.action == "show"))
async def show_day_schedule(callback: CallbackQuery, callback_data: LessonCb):
    kb = await build_schedule_keyboard(callback_data.day)
    week = get_week_list()
    await callback.message.edit_text(
        f"Расписание на день: {week[callback_data.day]}", reply_markup=kb
    )


@router.callback_query(Homework.filter(F.action == "homework"))
async def show_homework(callback: CallbackQuery, callback_data: Homework):
    await callback.message.edit_text(
        f"Домашняя работа по: {await get_subject_name(callback_data)}\n{await get_homework(callback_data)}",
        reply_markup=build_lesson_keyboard(callback_data),
    )


@router.callback_query(F.data == "close")
async def close(callback: CallbackQuery):
    await callback.message.delete()
