from typing import Dict, Any, List
from datetime import datetime, timedelta


def format_hourly_data(hourly_data: List[Dict[str, Any]], period: str = "tomorrow") -> str:
    """
    Универсальный форматтер для почасовых данных.

    Параметры:
        hourly_data: список почасовых словарей
        period: "yesterday" - данные за вчера
                "today" - данные за сегодня
                "tomorrow" - прогноз на завтра
                "next24h" - ближайшие 24 часа
    """
    if not hourly_data:
        return "❌ Нет данных"

    summary = format_summary_report(hourly_data, period=period)
    lines = [summary]
    lines.append("")

    for hour in hourly_data:
        time_str = datetime.fromisoformat(hour["time"]).strftime("%H:%M")
        hour_time = datetime.fromisoformat(hour["time"])
        now = datetime.now()
        sun_hours = hour.get("sunshine", 0) / 3600

        # Формируем каждую группу
        temp_group = f"t {hour['temp']:.0f}°C"
        precip_group = f"💧 {hour['precipitation']:.0f}мм"
        if hour_time > now and hour['precip_prob'] is not None:
            prob_group = f" ({hour['precip_prob']}%)"
        else:
            prob_group = ""
        sun_group = f"☀️ {sun_hours:.1f}ч"
        cloud_group = f"☁️ {hour['cloud']}%"
        hum_group = f"🌫 {hour['humidity']}%"
        wind_group = f"💨 {hour['wind_speed']:.0f}м/с"
        gust_group = f" ({hour['wind_gusts']:.0f}м/с)"

        # Первая строка: час + 4 группы
        line1 = (
            f"<pre>{time_str:<8}"
            f"{temp_group:<8}"
            f"{precip_group}{prob_group:<7}"
            f"{sun_group}"
        )
        lines.append(line1)

        # Вторая строка: остальные 4 группы
        line2 = (
            f"{cloud_group:<8}"
            f"{hum_group:<7}"
            f"{wind_group}{gust_group}</pre>"
        )
        lines.append(line2)

    return "\n".join(lines)


def format_summary_report(hourly_data: List[Dict[str, Any]], period: str = "tomorrow") -> str:
    """
    Форматирует агрегированные данные (с заголовком).
    Для yesterday: дождь = часы с осадками > 0
    Для прогнозов: дождь = часы с вероятностью >=20%
    """
    if not hourly_data:
        return "❌ Нет данных"

    # Заголовок
    first_time = datetime.fromisoformat(hourly_data[0]["time"])
    last_time = datetime.fromisoformat(hourly_data[-1]["time"])

    titles = {
        "yesterday": f"Отчет по погоде за вчера, {first_time.strftime('%d.%m')}",
        "today": f"Погода сегодня, {first_time.strftime('%d.%m')}",
        "tomorrow": f"Прогноз погоды на завтра, {first_time.strftime('%d.%m')}",
        "next24h": f"Прогноз на ближайшие сутки,\n{first_time.strftime('%d.%m %H:%M')} - {last_time.strftime('%d.%m %H:%M')}"
    }

    # Расчёт общих показателей (без учёта дождя)
    temps = [h["temp"] for h in hourly_data if h["temp"] is not None]
    humidities = [h["humidity"] for h in hourly_data if h["humidity"] is not None]
    wind_speeds = [h["wind_speed"] for h in hourly_data if h["wind_speed"] is not None]
    wind_gusts = [h["wind_gusts"] for h in hourly_data if h["wind_gusts"] is not None]
    clouds = [h["cloud"] for h in hourly_data if h["cloud"] is not None]

    if not temps:
        return "❌ Нет данных о температуре"

    total_precip = sum(h["precipitation"] for h in hourly_data if h["precipitation"] is not None)
    max_precip_prob = max([h["precip_prob"] for h in hourly_data if h["precip_prob"] is not None] or [0])
    avg_wind = sum(wind_speeds) / len(wind_speeds)
    max_gust = max(wind_gusts) if wind_gusts else 0
    max_humidity = max(humidities) if humidities else 0
    min_temp = min(temps)
    max_temp = max(temps)
    avg_cloud = sum(clouds) / len(clouds) if clouds else 0
    avg_temp = sum(temps) / len(temps)

    # Солнечные часы
    total_sun_seconds = sum(h.get("sunshine", 0) for h in hourly_data if h.get("sunshine") is not None)
    total_sun_hours = total_sun_seconds / 3600

    # --- ЛОГИКА ДОЖДЯ ---
    rainy_hours = []

    if period == "yesterday":
        # Вчера: показываем часы, когда ОСАДКИ БЫЛИ (> 0 мм)
        for h in hourly_data:
            if h["precipitation"] and h["precipitation"] > 0:
                hour_str = datetime.fromisoformat(h["time"]).strftime("%H:%M")
                rainy_hours.append(f"{hour_str} ({h['precipitation']:.1f}мм)")
    else:
        # Прогноз: показываем часы с ВЕРОЯТНОСТЬЮ >= 20%
        for h in hourly_data:
            prob = h["precip_prob"]
            if prob is not None and prob >= 20:
                hour_str = datetime.fromisoformat(h["time"]).strftime("%H:%M")
                rainy_hours.append(f"{hour_str} ({prob}%)")

    if rainy_hours:
        rainy_str = ", ".join(rainy_hours)
    else:
        rainy_str = "нет"

    # Строка осадков (с вероятностью только для прогнозов)
    if period == "yesterday":
        precip_line = f"Осадки: {total_precip:.1f} мм"
    else:
        max_precip_prob = max([h["precip_prob"] for h in hourly_data if h["precip_prob"] is not None] or [0])
        precip_line = f"Осадки: {total_precip:.1f} мм (вер. {max_precip_prob}%)"

    summary = (
        f"<b>{titles.get(period)}</b>\n\n"
        f"Температура: {min_temp:.0f}…{max_temp:.0f}°C (ср. {avg_temp:.0f})\n"
        f"{precip_line}\n"
        f"Солнца: {total_sun_hours:.1f} ч\n\n"
        f"Ветер ср: {avg_wind:.0f} м/с (порывы {max_gust:.0f} м/с)\n"
        f"Облачность ср: {avg_cloud:.0f}%\n"
        f"Влажность макс: {max_humidity:.0f}%\n\n"
        f"Дождь: {rainy_str}"
    )

    return summary