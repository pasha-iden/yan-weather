from datetime import datetime, timedelta

import sys
sys.path.append(".")
from tools.getter import get_weather_data
from tools.status_calculate import calculate_daily_stats
from tools.report_formatter import format_weather_report
from tools.keyboard import get_keyboard

async def send_daily_weather(bot, chat_id: str):
    """
    Функция для ежедневной отправки отчёта о погоде
    Вызывается по крону в 20:05
    """
    # print(f"🕐 Запуск ежедневного отчёта в {datetime.now().strftime('%H:%M')}")

    now = datetime.now()
    today_20 = now.replace(hour=20, minute=0, second=0, microsecond=0)

    # Отчёт за прошедшие сутки (вчера 20:00 -> сегодня 20:00)
    period_start = today_20 - timedelta(days=1)
    period_end = today_20

    # print(f"📊 Запрашиваю данные за период: {period_start} - {period_end}")

    weather_data = get_weather_data(period_start, period_end)

    if weather_data:
        stats = calculate_daily_stats(weather_data, period_end)
        report = format_weather_report(stats)

        try:
            await bot.send_message(chat_id, report, parse_mode="HTML", reply_markup=get_keyboard())
            # print(f"✅ Отчёт отправлен в чат {chat_id}")
        except Exception as e:
            # print(f"❌ Ошибка отправки сообщения: {e}")
            pass
    else:
        error_msg = "❌ Не удалось получить данные о погоде для ежедневного отчёта."
        # print(error_msg)
        try:
            await bot.send_message(chat_id, error_msg, parse_mode="HTML", reply_markup=get_keyboard())
        except Exception as e:
            # print(f"❌ Ошибка отправки сообщения об ошибке: {e}")
            pass