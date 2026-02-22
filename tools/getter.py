import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

# Координаты Тамани

TAMAN_LAT = 45.1649
TAMAN_LON = 36.7857

# ==================== ПОЛУЧЕНИЕ ПОГОДЫ ====================
def get_daily_weather_data(date_from: datetime, date_to: datetime) -> Optional[Dict[str, Any]]:
    """
    Получение данных о погоде за период в ДНЕВНОМ формате.
    Использует daily-параметры Open-Meteo вместо hourly.
    """

    try:
        start_date = date_from.strftime("%Y-%m-%d")
        end_date = date_to.strftime("%Y-%m-%d")

        params = {
            "latitude": TAMAN_LAT,
            "longitude": TAMAN_LON,
            "daily": [
                "temperature_2m_mean",  # средняя температура за день
                "relative_humidity_2m_mean",  # средняя влажность
                "precipitation_sum",  # сумма осадков
                "wind_speed_10m_max",  # макс. скорость ветра
                "wind_gusts_10m_max",  # макс. порывы
                "cloud_cover_mean",  # средняя облачность
                "sunshine_duration"  # продолжительность солнца
            ],
            "wind_speed_unit": "ms",
            "timezone": "Europe/Moscow",
            "start_date": start_date,
            "end_date": end_date
        }

        if date_from.date() < datetime.now().date():
            url = "https://archive-api.open-meteo.com/v1/archive"
        else:
            url = "https://api.open-meteo.com/v1/forecast"

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception:
        return None


def get_weather_data(mode: str = "forecast") -> Optional[Dict[str, Any]]:
    """
    Универсальная функция для получения погодных данных.

    Параметры:
        mode: "forecast" - прогноз на сегодня/завтра (2 дня)
              "yesterday" - исторические данные за вчера
    """
    try:
        # Базовые параметры для всех типов запросов
        base_params = {
            "latitude": TAMAN_LAT,
            "longitude": TAMAN_LON,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "precipitation_probability",
                "rain",
                "cloud_cover",
                "wind_speed_10m",
                "wind_gusts_10m",
                "wind_direction_10m",
                "pressure_msl",
                "sunshine_duration"
            ],
            "wind_speed_unit": "ms",
            "timezone": "Europe/Moscow",
        }

        if mode == "forecast":
            url = "https://api.open-meteo.com/v1/forecast"
            params = {**base_params, "forecast_days": 2}

        elif mode == "yesterday":
            url = "https://archive-api.open-meteo.com/v1/archive"
            yesterday = datetime.now() - timedelta(days=1)
            date_str = yesterday.strftime("%Y-%m-%d")
            params = {**base_params, "start_date": date_str, "end_date": date_str}

        else:
            raise ValueError(f"Unknown mode: {mode}")

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Error fetching {mode} data: {e}")
        return None