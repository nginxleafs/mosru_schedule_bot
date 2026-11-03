from dotenv import load_dotenv
import os

load_dotenv()

MOS_TOKEN = os.getenv("MOS_TOKEN")
PROFILE_ID = int(os.getenv("PROFILE_ID"))
CONTINGENT_GUID = os.getenv("CONTINGENT_GUID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]
