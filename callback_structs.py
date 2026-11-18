from aiogram.filters.callback_data import CallbackData


class LessonCb(CallbackData, prefix="lesson"):
    day: str
    action: str


class Homework(CallbackData, prefix="homework"):
    day: str
    subject: int
    action: str
