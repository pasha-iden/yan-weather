from datetime import datetime, timedelta
from typing import Dict, Any, List


def calculate_daily_stats(weather_data: Dict[str, Any], target_date: datetime) -> Dict[str, Any]:
    """
    Вычисление статистики за сутки (с 20:00 предыдущего дня до 20:00 текущего дня)
    """
    hourly_data = weather_data["hourly"]
    times = hourly_data["time"]

    yesterday_20 = (target_date - timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0)
    today_20 = target_date.replace(hour=20, minute=0, second=0, microsecond=0)

    start_index = None
    end_index = None

    # Ищем индексы начала и конца периода
    for i, time_str in enumerate(times):
        current_time = datetime.fromisoformat(time_str)

        if start_index is None and current_time >= yesterday_20:
            start_index = i

        if current_time <= today_20:
            end_index = i
        else:
            break

    if start_index is None or end_index is None or start_index > end_index:
        print(f"Error: Could not find time range. start={start_index}, end={end_index}")
        return {}

    # Вырезаем данные за нужный период
    temperatures = hourly_data["temperature_2m"][start_index:end_index + 1]
    humidities = hourly_data["relative_humidity_2m"][start_index:end_index + 1]
    precipitations = hourly_data["precipitation"][start_index:end_index + 1]
    wind_speeds = hourly_data["wind_speed_10m"][start_index:end_index + 1]
    wind_gusts = hourly_data["wind_gusts_10m"][start_index:end_index + 1]
    cloud_covers = hourly_data["cloud_cover"][start_index:end_index + 1]  # добавляем
    sunshine_durations = hourly_data["sunshine_duration"][start_index:end_index + 1]  # добавляем
    period_times = times[start_index:end_index + 1]

    # Основная статистика
    stats = {
        "date": target_date.strftime("%d.%m.%Y"),
        "avg_temperature": sum(temperatures) / len(temperatures),
        "avg_humidity": sum(humidities) / len(humidities),
        "total_precipitation": sum(precipitations),
        "avg_wind_speed": sum(wind_speeds) / len(wind_speeds),
        "max_wind_gust": max(wind_gusts),
        "avg_cloud_cover": sum(cloud_covers) / len(cloud_covers),  # средняя облачность
        "total_sunshine_seconds": sum(sunshine_durations),  # суммарное солнце в секундах
    }

    # Преобразуем секунды в часы для удобства
    stats["total_sunshine_hours"] = stats["total_sunshine_seconds"] / 3600

    # Температура в конкретные часы
    target_hours = [0, 5, 10, 15, 20]

    for hour in target_hours:
        target_time = target_date.replace(hour=hour, minute=0, second=0, microsecond=0)

        # Проверяем, что запрашиваемый час находится внутри нашего периода
        if yesterday_20 <= target_time <= today_20:
            # Ищем этот час в массиве period_times
            found = False
            for i, time_str in enumerate(period_times):
                current_time = datetime.fromisoformat(time_str)
                if current_time == target_time:
                    stats[f"temp_{hour:02d}00"] = temperatures[i]
                    # Можно также добавить облачность для этого часа, если нужно
                    # stats[f"cloud_{hour:02d}00"] = cloud_covers[i]
                    found = True
                    break

            if not found:
                stats[f"temp_{hour:02d}00"] = None
                print(f"Warning: Hour {hour}:00 not found in period_times")
        else:
            stats[f"temp_{hour:02d}00"] = None
            print(f"Warning: Hour {hour}:00 is outside the period")

    return stats


def calculate_forecast_period(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Извлекает из данных прогноз на 24 часа, начиная со следующего часа
    """
    hourly = data["hourly"]
    times = hourly["time"]

    now = datetime.now()
    current_hour_str = now.strftime("%Y-%m-%dT%H:00")

    # Находим индекс текущего часа
    current_index = None
    for i, t in enumerate(times):
        if t >= current_hour_str:
            current_index = i
            break

    if current_index is None:
        return []

    # Начинаем со следующего часа
    start_index = current_index + 1

    result = []
    for i in range(start_index, min(start_index + 24, len(times))):
        if hourly["temperature_2m"][i] is None:
            break

        hour_data = {
            "time": times[i],
            "temp": hourly["temperature_2m"][i],
            "humidity": hourly["relative_humidity_2m"][i],
            "precipitation": hourly["precipitation"][i],
            "precip_prob": hourly["precipitation_probability"][i],
            "rain": hourly["rain"][i],
            "cloud": hourly["cloud_cover"][i],
            "wind_speed": hourly["wind_speed_10m"][i],
            "wind_gusts": hourly["wind_gusts_10m"][i],
            "wind_dir": hourly["wind_direction_10m"][i],
            "pressure": hourly["pressure_msl"][i],
            "sunshine": hourly["sunshine_duration"][i]  # 👈 добавили
        }
        result.append(hour_data)

    return result