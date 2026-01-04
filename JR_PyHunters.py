from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import Command
from aiogram.types import Message
from handlers import main_router
import config
import misc


bot = Bot(token=config.BOT_TOKEN)

dp = Dispatcher()


async def start_bot():
    dp.startup.register(misc.on_start)
    dp.shutdown.register(misc.on_shutdown)
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass