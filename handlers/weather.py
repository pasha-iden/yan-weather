from aiogram import Router, types, F
from aiogram.types import CallbackQuery

from datetime import datetime, timedelta

import sys
sys.path.append(".")
from tools.getter import get_weather_data
from tools.status_calculate import calculate_daily_stats
from tools.report_formatter import format_weather_report
from tools.keyboard import get_keyboard

weather_router = Router()


@weather_router.callback_query(F.data == "weather_today")
async def weather_today(callback: CallbackQuery):
    """Погода за последние завершённые сутки (с 20:00 до 20:00)"""
    await callback.message.edit_text("🔍 Получаю данные о погоде...")

    now = datetime.now()
    today_20 = now.replace(hour=20, minute=0, second=0, microsecond=0)

    # ВСЕГДА берём последние завершённые сутки (с 20:00 до 20:00)
    if now < today_20:
        # Если сейчас меньше 20:00, берём позавчера 20:00 -> вчера 20:00
        period_end = today_20 - timedelta(days=1)  # вчера 20:00
        period_start = period_end - timedelta(days=1)  # позавчера 20:00
        report_date = period_end  # дата отчёта = вчера
    else:
        # Если сейчас больше или равно 20:00, берём вчера 20:00 -> сегодня 20:00
        period_end = today_20  # сегодня 20:00
        period_start = today_20 - timedelta(days=1)  # вчера 20:00
        report_date = period_end  # дата отчёта = сегодня

    weather_data = get_weather_data(period_start, period_end)
    if weather_data:
        stats = calculate_daily_stats(weather_data, report_date)
        report = format_weather_report(stats)
        await callback.message.edit_text(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )
    else:
        await callback.message.edit_text(
            "❌ Не удалось получить данные о погоде.",
            reply_markup=get_keyboard()
        )

    await callback.answer()