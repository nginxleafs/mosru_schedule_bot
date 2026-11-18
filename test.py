import asyncio
from datetime import datetime, timedelta

from schoolmospy import StudentClient

from constants import CONTINGENT_GUID, MOS_TOKEN, PROFILE_ID

client = StudentClient(token=MOS_TOKEN, profile_id=PROFILE_ID)


async def test_funciton():
    week = []
    for day in range(6):
        events = await client.events.get(
            datetime.today() + timedelta(days=day),
            datetime.today() + timedelta(days=day),
            contingent_guid=CONTINGENT_GUID,
        )
        week.append(events.model_dump())
    breakpoint()
    print(week)


async def main():
    await test_funciton()


if __name__ == "__main__":
    asyncio.run(main())
