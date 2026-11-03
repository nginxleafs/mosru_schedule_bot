from schoolmospy import StudentClient
from datetime import datetime, timedelta

from constants import MOS_TOKEN, PROFILE_ID, CONTINGENT_GUID
from callback_structs import Homework


async def get_data(day):
    day = datetime.today() + timedelta(days=day)
    client = StudentClient(
        token=MOS_TOKEN,
        profile_id=PROFILE_ID,
    )

    events = await client.events.get(
        from_date=day, to_date=day, contingent_guid=CONTINGENT_GUID
    )

    return events.model_dump()


async def get_homework(homework: Homework):
    data = await get_data(homework.day)
    result_homework = ""
    for i, o in enumerate(data["response"]):
        if i == homework.subject:
            if not o["homework"]["descriptions"]:
                result_homework = "Не задано"
            for d in o["homework"]["descriptions"]:
                result_homework += d
    return result_homework


async def get_subject_name(homework: Homework):
    data = await get_data(homework.day)
    result_subjects_name = ""
    for i, o in enumerate(data["response"]):
        if i == homework.subject:
            if o["subject_name"]:
                result_subjects_name = o["subject_name"]
    return result_subjects_name
