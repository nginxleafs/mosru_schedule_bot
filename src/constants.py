import os

from dotenv import load_dotenv

load_dotenv()


def required(key: str):
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return value


MOS_TOKEN: str = required("MOS_TOKEN")
PROFILE_ID: int = int(required("PROFILE_ID"))
CONTINGENT_GUID: str = required("CONTINGENT_GUID")
BOT_TOKEN: str = required("BOT_TOKEN")
ALLOWED_USER_IDS: list = list(required("ALLOWED_USER_IDS"))
LOG_LEVEL: str = required("LOG_LEVEL")

DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]
