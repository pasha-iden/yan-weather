from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура с inline-кнопками"""
    builder = InlineKeyboardBuilder()

    # Исторические отчеты - по два в ряд
    builder.row(
        InlineKeyboardButton(text="Год", callback_data="report_yearly"),
        InlineKeyboardButton(text="Квартал", callback_data="report_quarterly"),
        InlineKeyboardButton(text="Месяц", callback_data="report_monthly")
    )
    builder.row(
        InlineKeyboardButton(text="Вчера", callback_data="report_yesterday"),
        InlineKeyboardButton(text="Сегодня", callback_data="report_today"),
        InlineKeyboardButton(text="Завтра", callback_data="report_tomorrow")
    )

    builder.row(
        InlineKeyboardButton(text="Документация", callback_data="doc")
    )

    # Прогнозы - каждый на отдельной строке
    builder.row(
        InlineKeyboardButton(text="почасовой прогноз", callback_data="forecast_hourly")
    )
    builder.row(
        InlineKeyboardButton(text="ПРОГНОЗ НА СУТКИ", callback_data="forecast_tomorrow")
    )

    return builder.as_markup()