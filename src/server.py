import logging
import asyncio
import time
from datetime import datetime

from aiogram.types import CallbackQuery
from schoolmospy import StudentClient
from schoolmospy.utils.exceptions import APIError, AuthError, NotFoundError, ServerError
from exceptions import ScheduleUnavailableError

from callback_structs import Homework
from constants import CONTINGENT_GUID, MOS_TOKEN, PROFILE_ID


logger = logging.getLogger(__name__)

CACHE_TTL = 5 * 60

_cache = {}
_cache_lock = asyncio.Lock()


async def _get_data(requested_date_str: str) -> dict:
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
            logger.info("Requested data found in recent cache.")
            _, data = cached
            return data

        request_datetime = datetime.combine(requested_date, datetime.min.time())
        try:
            client = StudentClient(token=MOS_TOKEN, profile_id=PROFILE_ID)
            events = await asyncio.wait_for(
                client.events.get(
                    from_date=request_datetime,
                    to_date=request_datetime,
                    contingent_guid=CONTINGENT_GUID,
                ),
                timeout=10.0,
            )
        except AuthError:
            logger.error("Authentication error from school.mos.ru api.")
            raise
        except NotFoundError:
            logger.error("Not found error from school.mos.ru api.")
            raise
        except ServerError:
            logger.error("ServerError from school.mos.ru api.")
            raise
        except asyncio.TimeoutError:
            logger.error("School.mos.ru api server is not responding.")
            raise
        except Exception:
            raise
        data = events.model_dump()
        _cache[requested_date] = (time.monotonic() + CACHE_TTL, data)
        logger.info("Data received from server.")
        return data


async def get_data(requested_date_str: str, callback: CallbackQuery) -> dict:
    try:
        return await _get_data(requested_date_str)
    except asyncio.TimeoutError:
        await callback.message.answer(
            text="Время запроса превысило лимит.", show_alert=True
        )
        raise ScheduleUnavailableError
    except AuthError:
        await callback.message.answer(
            text="Ошибка авторизации:\n1 - Ваш токен просрочен\n2 - указан неверный profile id",
            show_alert=True,
        )

        raise ScheduleUnavailableError

    except ServerError:
        await callback.message.answer(
            text="Сервер не ответил: Сервер недоступен",
            show_alert=True,
        )
        raise ScheduleUnavailableError
    except NotFoundError:
        await callback.message.answer(
            text="Ресурс не найден, проверьте корректность GUID токена.",
            show_alert=True,
        )
        raise ScheduleUnavailableError

    except APIError as e:
        await callback.message.answer(
            text=f"Ошибка API: {e}\nСтатус код: {e.status_code}\n",
            show_alert=True,
        )
        raise ScheduleUnavailableError


def get_homework(homework: Homework, data: dict) -> str:
    lessons = data.get("response") or []
    if not 0 <= homework.subject_index < len(lessons):
        logger.error(
            f"Subject is out of range: subject index is {homework.subject_index}, but the length of received data is {len(lessons)}"
        )
        return "Урок не найден"
    lesson = lessons[homework.subject_index]
    homework_data = lesson.get("homework") or {}
    descriptions = homework_data.get("descriptions") or []
    result = "\n".join(descriptions) if descriptions else "Не задано"
    logger.info(
        f"Recognized homework: %s",
        result,
    )
    return result


def get_subject_name(homework: Homework, data: dict) -> str:
    lessons = data.get("response") or []
    if 0 <= homework.subject_index < len(lessons):
        lesson = lessons[homework.subject_index].get("subject_name") or "Не определен"
        logger.debug(f"Found subject name: {lesson}")
        return lesson

    logger.error("Unknown lesson with index=%s", homework.subject_index)
    return "Не определеный урок"
