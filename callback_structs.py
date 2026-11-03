from aiogram.filters.callback_data import CallbackData


class LessonCb(CallbackData, prefix="lesson"):
    day: int
    action: str


class Homework(CallbackData, prefix="homework"):
    day: int
    subject: int
    action: str
