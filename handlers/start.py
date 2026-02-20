from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import sys
sys.path.append(".")
from tools.keyboard import get_keyboard
from tools.user_storage import add_user

start_router = Router()

@start_router.message(CommandStart)
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "<b>Ян.Погода</b>\n\n"
        "Бот присылает прогноз погоды над виноградником Яна Владиславовича в Тамани на сутки в 5:50.\n\n"
        "У бота можно запросить:\n"
        "Прогноз на сутки\n"
        "Прогноз на сутки за каждый час\n"
        "Отчет по погоде за прошедшие сутки\n"
        "Отчет за прошлый месяц\n"
        "Отчет за прошлый квартал (сезон)\n"
        "Отчет за прошлый год\n\n"
        "В разработке:\n"
        "Прогноз на неделю\n"
        "Отчет за текущий месяц / последние 30 дней\n"
        "Агрегирование данных в отчетах за месяц, квартал, год\n\n"
        "<i>Данные предоставлены сервисом open-meteo.com для некоммерческого использования. </i>",
        parse_mode="HTML",
        reply_markup=get_keyboard()
    )
    add_user(message.from_user.id, message.message_id)


@start_router.callback_query(F.data == "doc")
async def cmd_start(callback: CallbackQuery):
    await callback.message.answer(
        "<b>Ян.Погода</b>\n\n"
        "Бот присылает прогноз погоды над виноградником Яна Владиславовича в Тамани на сутки в 5:50.\n\n"
        "У бота можно запросить:\n"
        "Прогноз на сутки\n"
        "Прогноз на сутки за каждый час\n"
        "Отчет по погоде за прошедшие сутки\n"
        "Отчет за прошлый месяц\n"
        "Отчет за прошлый квартал (сезон)\n"
        "Отчет за прошлый год\n\n"
        "В разработке:\n"
        "Прогноз на неделю\n"
        "Отчет за текущий месяц / последние 30 дней\n"
        "Агрегирование данных в отчетах за месяц, квартал, год\n\n"
        "<i>Данные предоставлены сервисом open-meteo.com для некоммерческого использования. </i>",
        parse_mode="HTML",
        reply_markup=get_keyboard()
    )
    add_user(callback.message.from_user.id, callback.message.message_id)