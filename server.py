import asyncio
import time
from datetime import datetime

from schoolmospy import StudentClient

from callback_structs import Homework
from constants import CONTINGENT_GUID, MOS_TOKEN, PROFILE_ID

CACHE_TTL = 5 * 60

_cache = {}
_cache_lock = asyncio.Lock()


async def get_data(requested_date_str):
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

        events = await client.events.get(
            from_date=request_datetime,
            to_date=request_datetime,
            contingent_guid=CONTINGENT_GUID,
        )
        data = events.model_dump()
        _cache[requested_date] = (time.monotonic() + CACHE_TTL, data)
        return data


async def get_homework(homework: Homework, data):
    result_homework = ""
    for i, o in enumerate(data["response"]):
        if i == homework.subject:
            if not o["homework"]["descriptions"]:
                result_homework = "Не задано"
            for d in o["homework"]["descriptions"]:
                result_homework += d
    return result_homework


async def get_subject_name(homework: Homework, data):
    result_subjects_name = ""
    for i, o in enumerate(data["response"]):
        if i == homework.subject:
            if o["subject_name"]:
                result_subjects_name = o["subject_name"]
    return result_subjects_name
