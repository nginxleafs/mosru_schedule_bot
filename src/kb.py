from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from callback_structs import Day, Homework, Lesson
from instructions import info_button_text, check_schedule_button_text
from utils import get_week_list


def build_main_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=check_schedule_button_text)
    builder.button(text=info_button_text)
    return builder.as_markup(resize_keyboard=True)


def build_subjects_kb(data: dict, date: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    subjects = []
    for d in data["response"]:
        subjects.append(d["subject_name"])
    for enum, o in enumerate(subjects):
        builder.button(
            text=o,
            callback_data=Homework(
                date=date, subject_index=enum, action="show_subject_homework"
            ),
        )
    builder.button(text="Назад ⬅️", callback_data="back_to_week")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def build_homework_kb(homework: Homework) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад ⬅️",
        callback_data=Lesson(
            date=homework.date,
            action="back_to_subjects",
        ),
    )
    return builder.as_markup(resize_keyboard=True)


def build_week_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for d, name in enumerate(get_week_list()):
        date = str((datetime.today() + timedelta(days=d)).date())
        builder.button(text=name, callback_data=Day(date=date, action="show_subjects"))
    builder.button(text="Закрыть ❌", callback_data="close")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
