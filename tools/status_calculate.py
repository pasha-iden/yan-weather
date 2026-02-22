from datetime import datetime, timedelta
from typing import Dict, Any, List


from datetime import datetime
from typing import Dict, Any, List, Optional


def calculate_hourly_data(data: Dict[str, Any], mode: str = "forecast", start_mode: str = "now") -> Optional[List[Dict[str, Any]]]:
    """
    Универсальная функция для обработки почасовых данных.
    """
    if not data or "hourly" not in data:
        return None

    hourly = data["hourly"]
    times = hourly["time"]

    # Определяем индексы для выборки
    if mode == "yesterday":
        # Все 24 часа
        start_idx = 0
        end_idx = len(times)

    elif mode == "forecast":
        now = datetime.now()

        # Определяем целевую дату-время для старта
        if start_mode == "now":
            target_time = now
        elif start_mode == "today":
            target_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif start_mode == "tomorrow":
            target_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Unknown start_mode: {start_mode}")

        target_str = target_time.strftime("%Y-%m-%dT%H:00")

        # Находим индекс
        start_idx = None
        for i, t in enumerate(times):
            if t >= target_str:
                start_idx = i
                break

        if start_idx is None:
            return []

        # Для режима "now" начинаем со следующего часа
        if start_mode == "now":
            start_idx += 1

        end_idx = min(start_idx + 24, len(times))

    else:
        raise ValueError(f"Unknown mode: {mode}")

    # Единый блок сбора данных
    result = []
    for i in range(start_idx, end_idx):
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
            "sunshine": hourly["sunshine_duration"][i]
        }
        result.append(hour_data)

    return result