from constants import DAYS
from datetime import datetime


def get_week_list():
    today = datetime.now().weekday()
    week = []
    for d in range(7):
        if today == 7:
            today = 0
        week.append(DAYS[today])
        today += 1
    return week
