from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import sys
sys.path.append(".")
from tools.keyboard import get_keyboard

start_router = Router()

@start_router.message(CommandStart)
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    print(message.from_user.id)
    await message.answer(
        "<b>Ян.Погода</b>\n\n"
        "Бот присылает отчёт по погоде за последние сутки в 20:05.\n"
        "Можно запросить отчёт по погоде за последние сутки вручную.",
        parse_mode="HTML",
        reply_markup=get_keyboard()
    )