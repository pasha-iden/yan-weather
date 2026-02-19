from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура с inline-кнопками"""
    builder = InlineKeyboardBuilder()

    # Первая кнопка в отдельном ряду
    builder.row(
        InlineKeyboardButton(text="Отчет за сутки", callback_data="report_daily")
    )
    builder.row(
        InlineKeyboardButton(text="Отчет за месяц", callback_data="report_monthly")
    )
    builder.row(
        InlineKeyboardButton(text="Отчет за квартал", callback_data="report_quarterly")
    )
    builder.row(
        InlineKeyboardButton(text="Отчет за год", callback_data="report_yearly")
    )

    # # Вторая кнопка в отдельном ряду
    # builder.row(
    #     InlineKeyboardButton(text="Документация", callback_data="docs")
    # )

    return builder.as_markup()
