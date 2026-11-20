from datetime import datetime, timedelta

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from schoolmospy.utils.exceptions import AuthError

from callback_structs import Homework, LessonCb
from instructions import info_button, watch_for_weekdays_button
from server import ScheduleUnavailableError, get_data
from utils import get_week_list


def build_main_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text=watch_for_weekdays_button)
    builder.button(text=info_button)
    return builder.as_markup(resize_keyboard=True)


async def build_schedule_keyboard(day):
    builder = InlineKeyboardBuilder()
    try:
        data = await get_data(day)
    except ScheduleUnavailableError:
        builder.button(text="Расписание недоступно, попробуйте позже.")
        builder.button(text="Назад ⬅️", callback_data="back_to_week")
        builder.adjust(1)
        return builder.as_markup()
    except AuthError:
        builder.button(text="Срок действия вашего токена истек.", callback_data="error")
        builder.button(text="Назад ⬅️", callback_data="back_to_week")
        builder.adjust(1)
        return builder.as_markup()

    subjects = []
    for d in data["response"]:
        subjects.append(d["subject_name"])
    for enum, o in enumerate(subjects):
        builder.button(
            text=o,
            callback_data=Homework(day=day, subject=enum, action="homework"),
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
        date = str((datetime.today() + timedelta(days=d)).date())
        builder.button(text=name, callback_data=LessonCb(day=date, action="show"))
    builder.button(text="Закрыть ❌", callback_data="close")
    builder.adjust(1)
    return builder.as_markup()
