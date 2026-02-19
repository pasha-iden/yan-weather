from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура с inline-кнопками"""
    builder = InlineKeyboardBuilder()

    # Первая кнопка в отдельном ряду
    builder.row(
        InlineKeyboardButton(text="Погода за сутки", callback_data="weather_today")
    )

    # # Вторая кнопка в отдельном ряду
    # builder.row(
    #     InlineKeyboardButton(text="Документация", callback_data="docs")
    # )

    return builder.as_markup()
