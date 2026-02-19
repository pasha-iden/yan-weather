import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Координаты Тамани
TAMAN_LAT = 45.2119
TAMAN_LON = 36.7163

# ==================== ПОЛУЧЕНИЕ ПОГОДЫ ====================
def get_weather_data(date_from: datetime, date_to: datetime) -> Optional[Dict[str, Any]]:
    """
    Получение почасовых данных о погоде за указанный период.
    """
    TAMAN_LAT = 45.2119
    TAMAN_LON = 36.7163

    try:
        start_date = date_from.strftime("%Y-%m-%d")
        end_date = date_to.strftime("%Y-%m-%d")

        params = {
            "latitude": TAMAN_LAT,
            "longitude": TAMAN_LON,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_gusts_10m",
                "cloud_cover",  # добавляем облачность
                "sunshine_duration"  # добавляем продолжительность солнца
            ],
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