from datetime import datetime
import json

from constants import DAYS


def get_week_list():
    today = datetime.now().weekday()
    return [DAYS[(today + offset) % 7] for offset in range(7)]
