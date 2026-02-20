from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура с inline-кнопками"""
    builder = InlineKeyboardBuilder()

    # Исторические отчеты - по два в ряд
    builder.row(
        InlineKeyboardButton(text="Отчет за год", callback_data="report_yearly"),
        InlineKeyboardButton(text="Отчет за квартал", callback_data="report_quarterly")
    )
    builder.row(
        InlineKeyboardButton(text="Отчет за месяц", callback_data="report_monthly"),
        InlineKeyboardButton(text="Отчет за сутки", callback_data="report_daily")
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