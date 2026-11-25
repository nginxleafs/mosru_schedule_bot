import asyncio

from aiogram import Bot, Dispatcher

from callbacks import router as callbacks_router
from constants import BOT_TOKEN, LOG_LEVEL
from messages import router as messages_router

import logging

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router=callbacks_router)
    dp.include_router(router=messages_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
