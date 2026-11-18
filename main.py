import asyncio

from aiogram import Bot, Dispatcher

from callbacks import router as callbacks_router
from constants import BOT_TOKEN
from messages import router as messages_router


async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router=callbacks_router)
    dp.include_router(router=messages_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
