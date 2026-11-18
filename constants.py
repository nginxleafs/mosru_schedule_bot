import os

from dotenv import load_dotenv

load_dotenv()


def required(key: str):
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return value


MOS_TOKEN = required("MOS_TOKEN")
PROFILE_ID = int(required("PROFILE_ID"))
CONTINGENT_GUID = required("CONTINGENT_GUID")
BOT_TOKEN = required("BOT_TOKEN")

DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]

OWNER_ID = [5727422326]
