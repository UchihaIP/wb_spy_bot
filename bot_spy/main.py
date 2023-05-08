import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from core.config import settings
from core.logger import logger
from core.handlers import Handers
from core.spy_proccess import spy_proccess

tasks: dict[str, asyncio.Task] = {}

async def register_all_handlers(bot, dp):
    logger.debug("Register handlers...")
    handlers = Handers(bot=bot, dp=dp)
    await handlers.register_handlers()
    logger.debug("Register handlers: Done!")


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    logger.info("Bot started")

    
    await register_all_handlers(bot, dp)
    tasks["spy_proc"] = asyncio.create_task(spy_proccess(bot=bot))

    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        tasks["spy_proc"].cancel()
        logger.info("Bot Closed")
