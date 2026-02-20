import asyncio
from zoneinfo import ZoneInfo

import aiocron
from aiogram import Bot, Dispatcher

from handlers.start import start_router
from handlers.weather import weather_router
from cron.daily_sender import send_daily_weather
from tools.user_storage import load_users, save_users

import os

if os.path.exists('config.py'): from config import BOT_TOKEN
else: BOT_TOKEN = os.getenv("BOT_TOKEN")


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(start_router, weather_router)


async def on_startup():
    load_users(os.path.exists('config.py'))
    aiocron.crontab('5 20 * * *', tz=ZoneInfo('Europe/Moscow'))(
        lambda: send_daily_weather(bot) ).start()


async def on_shutdown():
    save_users(os.path.exists('config.py'))
    await bot.session.close()


dp.startup.register(on_startup)
async def main():
    try: await dp.start_polling(bot)
    finally: await on_shutdown()


if __name__ == "__main__":
    try: asyncio.run(main())
    except: pass