from datetime import datetime
from typing import Dict, Any, List


def extract_daily_data(weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Извлекает данные из ответа Open-Meteo в формате daily.
    Возвращает список словарей с данными за каждый день.
    """
    if "daily" not in weather_data:
        return []

    daily = weather_data["daily"]
    times = daily["time"]

    result = []
    for i, date_str in enumerate(times):
        # Open-Meteo возвращает даты в формате "2025-02-20"
        day_data = {
            "date": datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y"),
            "avg_temp": daily["temperature_2m_mean"][i],
            "avg_humidity": daily["relative_humidity_2m_mean"][i],
            "total_precipitation": daily["precipitation_sum"][i],
            "max_wind": daily["wind_speed_10m_max"][i],
            "max_gust": daily["wind_gusts_10m_max"][i],
            "avg_cloud": daily["cloud_cover_mean"][i],
            "total_sun_hours": daily["sunshine_duration"][i] / 3600,  # секунды в часы
        }
        result.append(day_data)

    return result