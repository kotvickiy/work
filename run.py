import asyncio

from aiogram import Bot, Dispatcher

from config import TG_TOKEN
from app.handlers import router


bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
