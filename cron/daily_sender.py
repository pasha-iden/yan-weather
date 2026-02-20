from datetime import datetime, timedelta

import sys
sys.path.append(".")
from tools.getter import get_weather_data, get_hourly_forecast
from tools.status_calculate import calculate_daily_stats, calculate_forecast_period
from tools.report_formatter import format_weather_report, format_tomorrow_forecast
from tools.keyboard import get_keyboard
from tools.user_storage import get_all_users

async def send_daily_weather(bot):

    now = datetime.now()
    today_20 = now.replace(hour=20, minute=0, second=0, microsecond=0)

    period_start = today_20 - timedelta(days=1)
    period_end = today_20

    users = get_all_users()
    if users:

        weather_data = get_weather_data(period_start, period_end)
        if weather_data:
            stats = calculate_daily_stats(weather_data, period_end)
            report = format_weather_report(stats)

            for user_id in users.keys():
                try:
                    await bot.send_message(int(user_id), report, parse_mode="HTML", reply_markup=get_keyboard())
                except Exception as e:
                    pass

        else:
            error_msg = "❌ Не удалось получить данные о погоде для ежедневного отчёта."
            for user_id in users.keys():
                try:
                    await bot.send_message(int(user_id), error_msg, parse_mode="HTML", reply_markup=get_keyboard())
                except:
                    pass


async def send_tomorrow_forecast(bot):

    users = get_all_users()
    if users:

        forecast_data = get_hourly_forecast()
        if forecast_data:
            hourly_data = calculate_forecast_period(forecast_data)

            report = format_tomorrow_forecast(hourly_data)

            for user_id in users.keys():
                try:
                    await bot.send_message(int(user_id), report, parse_mode="HTML", reply_markup=get_keyboard())
                except Exception as e:
                    pass

        else:
            error_msg = "❌ Нет данных прогноза"
            for user_id in users.keys():
                try:
                    await bot.send_message(int(user_id), error_msg, parse_mode="HTML", reply_markup=get_keyboard())
                except:
                    pass