from typing import Dict, Any, List
from datetime import datetime, timedelta


def format_weather_report(stats: Dict[str, Any]) -> str:
    """
    Форматирование отчёта о погоде
    """
    if not stats:
        return "Не удалось получить данные о погоде"

    def format_temp(value):
        if value is None:
            return "—"
        return f"{value:.1f}°C"

    def format_num(value, suffix="", decimals=1):
        if isinstance(value, (int, float)):
            return f"{value:.{decimals}f}{suffix}"
        return str(value)

    # Функция для форматирования облачности с эмодзи
    def format_cloud(value):
        if value is None:
            return "—"

        if value < 10:
            return f"{value:.0f}% Ясно"
        elif value < 30:
            return f"{value:.0f}% Малооблачно"
        elif value < 60:
            return f"{value:.0f}% Облачно с прояснениями"
        elif value < 90:
            return f"{value:.0f}% Пасмурно"
        else:
            return f"{value:.0f}% Сплошная облачность"

    # Функция для форматирования солнечных часов
    def format_sunshine(hours):
        if hours is None:
            return "—"

        # Округляем до 1 знака
        hours_rounded = round(hours, 1)

        # Выбираем эмодзи в зависимости от продолжительности
        if hours_rounded < 1:
            return f"{hours_rounded} ч"
        elif hours_rounded < 3:
            return f"{hours_rounded} "
        elif hours_rounded < 6:
            return f"{hours_rounded} ч"
        elif hours_rounded < 9:
            return f"{hours_rounded} ч"
        else:
            return f"{hours_rounded} ч"

    today = datetime.now().strftime("%d.%m.%Y")
    report_date = datetime.strptime(stats['date'], "%d.%m.%Y")
    previous_date = (report_date - timedelta(days=1)).strftime("%d.%m.%Y")

    report = [
        f"<b>Погода в Тамани за 20:00 {previous_date} - 20:00 {stats['date']}</b>\n",
        f"<b>Средние показатели за сутки:</b>",
        f"• Температура: {format_num(stats['avg_temperature'], '°C')}",
        f"• Влажность: {format_num(stats['avg_humidity'], '%', 0)}",
        f"• Осадки: {format_num(stats['total_precipitation'], ' мм', 1)}",
        f"• Ветер (средний): {format_num(stats['avg_wind_speed'], ' м/с', 1)}",
        f"• Порывы (макс): {format_num(stats['max_wind_gust'], ' м/с', 1)}",
        f"• Облачность: {format_cloud(stats['avg_cloud_cover'])}",
        f"• Солнце: {format_sunshine(stats['total_sunshine_hours'])}\n",
        f"<b>Температура в отдельные часы:</b>",
        f"• 00:00 — {format_temp(stats.get('temp_0000'))}",
        f"• 05:00 — {format_temp(stats.get('temp_0500'))}",
        f"• 10:00 — {format_temp(stats.get('temp_1000'))}",
        f"• 15:00 — {format_temp(stats.get('temp_1500'))}",
        f"• 20:00 — {format_temp(stats.get('temp_2000'))}",
        f"\nДанные о погоде за сегодня, {today}, будут готовы в 20:05."
    ]

    return "\n".join(report)


def format_hourly_forecast(forecast_data: List[Dict[str, Any]]) -> str:
    """
    Форматирует почасовой прогноз для отправки в Telegram
    """
    if not forecast_data:
        return "❌ Нет данных прогноза"

    lines = ["<b>Прогноз на 24 часа</b>\n"]

    # Сначала почасовые данные
    for hour in forecast_data:
        time_str = datetime.fromisoformat(hour["time"]).strftime("%H:%M %d.%m")

        # Вероятность осадков - ВСЕГДА выводим
        prob_str = f" ({hour['precip_prob']}%)"

        def get_wind_direction(degrees: float) -> str:
            """Преобразует градусы в направление ветра"""
            directions = [
                "С", "СВ", "В", "ЮВ",
                "Ю", "ЮЗ", "З", "СЗ"
            ]
            if degrees is None:
                return "—"
            index = round(degrees / 45) % 8
            return directions[index]

        line = (
            f"<b>{time_str}</b>\n"
            f"Температура: {hour['temp']:.1f}°C\n"
            f"Влажность: {hour['humidity']}%\n"
            f"Осадки: {hour['precipitation']:.1f} мм\n"
            f"Вероятность осадков: {prob_str}\n"
            f"Ветер: {hour['wind_speed']:.1f} м/с (порывы {hour['wind_gusts']:.1f}) {get_wind_direction(hour['wind_dir'])}\n"
            f"Облачность: {hour['cloud']}%\n"
            f"Давление: {hour['pressure']:.0f} гПа\n"
        )
        lines.append(line)

    summary = format_tomorrow_forecast(forecast_data)
    lines.append(summary)

    return "\n".join(lines)


def format_tomorrow_forecast(forecast_data: List[Dict[str, Any]]) -> str:
    """
    Форматирует прогноз на 24 часа (только агрегированные данные)
    """
    if not forecast_data:
        return "❌ Нет данных прогноза"

    # Расчет всех показателей
    temps = [h["temp"] for h in forecast_data]
    humidities = [h["humidity"] for h in forecast_data]
    wind_speeds = [h["wind_speed"] for h in forecast_data]
    wind_gusts = [h["wind_gusts"] for h in forecast_data]
    clouds = [h["cloud"] for h in forecast_data]
    precip_probs = [h["precip_prob"] for h in forecast_data]

    total_precip = sum(h["precipitation"] for h in forecast_data)
    max_precip_prob = max(precip_probs)
    avg_wind = sum(wind_speeds) / len(wind_speeds)
    max_gust = max(wind_gusts)
    max_humidity = max(humidities)
    min_temp = min(temps)
    max_temp = max(temps)
    avg_cloud = sum(clouds) / len(clouds)
    avg_temp = sum(temps) / len(temps)

    # Солнечные часы
    total_sun_seconds = sum(h.get("sunshine", 0) for h in forecast_data)
    total_sun_hours = total_sun_seconds / 3600

    # Часы с вероятностью дождя >=20%
    rainy_hours = []
    low_prob_hours = []

    for h in forecast_data:
        prob = h["precip_prob"]
        if prob >= 20:
            hour_str = datetime.fromisoformat(h["time"]).strftime("%H:%M")
            rainy_hours.append(f"{hour_str} ({prob}%)")
        elif 5 < prob < 20:
            low_prob_hours.append(prob)

    if rainy_hours:
        rainy_str = ", ".join(rainy_hours)
    elif low_prob_hours:
        rainy_str = "вероятность меньше 20%"
    else:
        rainy_str = "нет"

    summary = (
        f"<b>Прогноз на сутки:</b>\n\n"
        f"Температура: {min_temp:.1f}…{max_temp:.1f}°C (ср. {avg_temp:.1f})\n"
        f"Осадки: {total_precip:.1f} мм (вер. {max_precip_prob}%)\n"
        f"Солнца: {total_sun_hours:.1f} ч\n\n"
        
        f"Ветер ср: {avg_wind:.1f} м/с (порывы {max_gust:.1f})\n"
        f"Облачность ср: {avg_cloud:.0f}%\n"
        f"Влажность макс: {max_humidity:.0f}%\n\n"
        
        f"Дождь: {rainy_str}"
    )

    return summary