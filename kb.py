from server import get_data
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from callback_structs import Homework, LessonCb
from utils import get_week_list

from instructions import watch_for_weekdays_button, info_button


def build_main_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text=watch_for_weekdays_button)
    builder.button(text=info_button)
    return builder.as_markup(resize_keyboard=True)


async def build_schedule_keyboard(day):
    data = await get_data(day)
    subjects = []
    for d in data["response"]:
        subjects.append(d["subject_name"])
    builder = InlineKeyboardBuilder()
    for enum, o in enumerate(subjects):
        builder.button(
            text=o, callback_data=Homework(day=day, subject=enum, action="homework")
        )
    builder.button(text="Назад ⬅️", callback_data="back_to_week")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def build_lesson_keyboard(homework: Homework):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад ⬅️",
        callback_data=Homework(
            day=homework.day,
            subject=homework.subject,
            action="back_to_lessons",
        ),
    )
    return builder.as_markup()


def build_days_kb():
    builder = InlineKeyboardBuilder()
    for d, name in enumerate(get_week_list()):
        builder.button(text=name, callback_data=LessonCb(day=d, action="show"))
    builder.button(text="Закрыть ❌", callback_data="close")
    builder.adjust(1)
    return builder.as_markup()
