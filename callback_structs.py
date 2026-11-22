from aiogram.filters.callback_data import CallbackData


class Day(CallbackData, prefix="day"):
    date: str
    action: str


class Homework(CallbackData, prefix="homework"):
    date: str
    subject_index: int
    action: str


class Lesson(CallbackData, prefix="lesson"):
    date: str
    action: str
