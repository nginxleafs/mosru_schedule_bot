import asyncio
import time
from datetime import datetime

from schoolmospy import StudentClient

from callback_structs import Homework
from constants import CONTINGENT_GUID, MOS_TOKEN, PROFILE_ID


class ScheduleUnavailableError(Exception):
    """Не удалось получить расписание."""


CACHE_TTL = 5 * 60

_cache = {}
_cache_lock = asyncio.Lock()


async def get_data(requested_date_str: str) -> dict:
    requested_date = datetime.fromisoformat(requested_date_str)
    async with _cache_lock:
        now = time.monotonic()

        expired_dates = [
            date for date, (expires_at, _) in _cache.items() if expires_at <= now
        ]
        for date in expired_dates:
            del _cache[date]

        cached = _cache.get(requested_date)
        if cached is not None:
            _, data = cached
            return data

        client = StudentClient(token=MOS_TOKEN, profile_id=PROFILE_ID)
        request_datetime = datetime.combine(requested_date, datetime.min.time())
        try:
            events = await client.events.get(
                from_date=request_datetime,
                to_date=request_datetime,
                contingent_guid=CONTINGENT_GUID,
            )
        except Exception as e:
            raise ScheduleUnavailableError("Не удалось получить расписание") from e
        data = events.model_dump()
        _cache[requested_date] = (time.monotonic() + CACHE_TTL, data)
        return data


async def get_homework(homework: Homework, data: dict) -> str:
    lessons = data.get("response") or []
    if not 0 <= homework.subject < len(lessons):
        breakpoint()
        return "Урок не найден"
    lesson = lessons[homework.subject]
    homework_data = lesson.get("homework") or {}
    descriptions = homework_data.get("descriptions") or []
    return "\n".join(descriptions) if descriptions else "Не задано"


async def get_subject_name(homework: Homework, data: dict) -> str:
    lessons = data.get("response") or []
    if 0 <= homework.subject < len(lessons):
        return lessons[homework.subject].get("subject_name") or "Не определен"

    return "Не определен"
