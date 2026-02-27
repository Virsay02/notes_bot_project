from aiogram import Dispatcher, Bot
import asyncio
import logging
import  os
from dotenv import  load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from routers import  router as main_router

load_dotenv()
dp = Dispatcher()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот закончил работу")
