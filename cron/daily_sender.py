from datetime import datetime, timedelta

import sys
sys.path.append(".")
from tools.getter import get_weather_data
from tools.status_calculate import calculate_hourly_data
from tools.report_formatter import format_summary_report
from tools.keyboard import get_keyboard
from tools.user_storage import get_all_users


async def send_tomorrow_forecast(bot):

    users = get_all_users()
    if users:

        forecast_data = get_weather_data("forecast")
        if forecast_data:
            hourly_data = calculate_hourly_data(forecast_data, "forecast", "now")

            report = format_summary_report(hourly_data, "next24h")

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