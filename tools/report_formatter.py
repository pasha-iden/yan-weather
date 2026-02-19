from typing import Dict, Any
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