from aiogram import Router, types, F
from aiogram.types import CallbackQuery

from datetime import datetime, timedelta

import sys
sys.path.append(".")
from tools.getter import get_weather_data
from tools.status_calculate import calculate_hourly_data
from tools.report_formatter import format_hourly_data, format_summary_report
from tools.report_generator import generate_report_files
from tools.keyboard import get_keyboard

weather_router = Router()


@weather_router.callback_query(F.data == "report_yesterday")
async def report_yesterday(callback: CallbackQuery):

    try:
        # Получаем сырые данные
        raw_data = get_weather_data("yesterday")
        if not raw_data:
            await callback.message.answer(
                "❌ Не удалось получить данные за вчера",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Преобразуем в список почасовых словарей
        hourly_data = calculate_hourly_data(raw_data, "yesterday")
        if not hourly_data:
            await callback.message.answer(
                "❌ Ошибка обработки данных",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Форматируем почасовые данные
        report = format_hourly_data(hourly_data, "yesterday")

        # Отправляем готовый отчёт
        await callback.message.answer(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()


@weather_router.callback_query(F.data == "report_today")
async def report_today(callback: CallbackQuery):

    try:
        # Получаем сырые данные
        raw_data = get_weather_data("forecast")
        if not raw_data:
            await callback.message.answer(
                "❌ Не удалось получить данные за вчера",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Преобразуем в список почасовых словарей
        hourly_data = hourly_data = calculate_hourly_data(raw_data, "forecast", "today")
        if not hourly_data:
            await callback.message.answer(
                "❌ Ошибка обработки данных",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Форматируем почасовые данные
        report = format_hourly_data(hourly_data, "today")

        # Отправляем готовый отчёт
        await callback.message.answer(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()


@weather_router.callback_query(F.data == "report_tomorrow")
async def report_tomorrow(callback: CallbackQuery):

    try:
        # Получаем сырые данные
        raw_data = get_weather_data("forecast")
        if not raw_data:
            await callback.message.answer(
                "❌ Не удалось получить данные за вчера",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Преобразуем в список почасовых словарей
        hourly_data = calculate_hourly_data(raw_data, "forecast", "tomorrow")
        if not hourly_data:
            await callback.message.answer(
                "❌ Ошибка обработки данных",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Форматируем почасовые данные
        report = format_hourly_data(hourly_data, "tomorrow")

        # Отправляем готовый отчёт
        await callback.message.answer(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()




@weather_router.callback_query(lambda c: c.data == "report_monthly")
async def report_monthly(callback: CallbackQuery):
    """Отчет за прошлый месяц в Excel и PDF"""

    try:
        # Определяем период (прошлый месяц)
        today = datetime.now()
        if today.month == 1:
            year = today.year - 1
            month = 12
        else:
            year = today.year
            month = today.month - 1

        # Генерируем отчеты в памяти
        excel_bytes, pdf_bytes, period_name = generate_report_files(year, month=month)

        from aiogram.types import BufferedInputFile, InputMediaDocument

        pdf_file = BufferedInputFile(
            pdf_bytes.getvalue(),
            filename=f"weather_{year}_{month:02d}.pdf"
        )

        excel_file = BufferedInputFile(
            excel_bytes.getvalue(),
            filename=f"weather_{year}_{month:02d}.xlsx"
        )

        # Медиагруппа БЕЗ caption
        media_group = [
            InputMediaDocument(media=pdf_file),
            InputMediaDocument(media=excel_file)
        ]

        await callback.message.answer_media_group(media_group)

        # Отдельное сообщение с текстом и кнопками
        await callback.message.answer(
            f"Отчет за {period_name}",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка при генерации отчета: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()


@weather_router.callback_query(lambda c: c.data == "report_quarterly")
async def report_quarterly(callback: CallbackQuery):
    """Отчет за прошлый квартал в Excel и PDF"""

    try:
        # Определяем прошлый квартал
        today = datetime.now()
        current_quarter = (today.month - 1) // 3 + 1

        if current_quarter == 1:
            year = today.year - 1
            quarter = 4
        else:
            year = today.year
            quarter = current_quarter - 1

        # Генерируем отчеты в памяти
        excel_bytes, pdf_bytes, period_name = generate_report_files(year, quarter=quarter)

        from aiogram.types import BufferedInputFile, InputMediaDocument

        pdf_file = BufferedInputFile(
            pdf_bytes.getvalue(),
            filename=f"weather_{year}_Q{quarter}.pdf"
        )

        excel_file = BufferedInputFile(
            excel_bytes.getvalue(),
            filename=f"weather_{year}_Q{quarter}.xlsx"
        )

        # Медиагруппа БЕЗ caption
        media_group = [
            InputMediaDocument(media=pdf_file),
            InputMediaDocument(media=excel_file)
        ]

        await callback.message.answer_media_group(media_group)

        # Отдельное сообщение с текстом и кнопками
        await callback.message.answer(
            f"Отчет за {period_name}",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка при генерации отчета: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()


@weather_router.callback_query(lambda c: c.data == "report_yearly")
async def report_yearly(callback: CallbackQuery):
    """Отчет за прошлый год в Excel и PDF"""

    try:
        # Прошлый год
        year = datetime.now().year - 1

        # Генерируем отчеты в памяти
        excel_bytes, pdf_bytes, period_name = generate_report_files(year)

        from aiogram.types import BufferedInputFile, InputMediaDocument

        pdf_file = BufferedInputFile(
            pdf_bytes.getvalue(),
            filename=f"weather_{year}.pdf"
        )

        excel_file = BufferedInputFile(
            excel_bytes.getvalue(),
            filename=f"weather_{year}.xlsx"
        )

        # Медиагруппа БЕЗ caption
        media_group = [
            InputMediaDocument(media=pdf_file),
            InputMediaDocument(media=excel_file)
        ]

        await callback.message.answer_media_group(media_group)

        # Отдельное сообщение с текстом и кнопками
        await callback.message.answer(
            f"Отчет за {period_name}",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка при генерации отчета: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()





@weather_router.callback_query(lambda c: c.data == "forecast_hourly")
async def forecast_hourly(callback: CallbackQuery):
    """Почасовой прогноз на сутки вперед с 6 утра"""

    try:
        # Получаем данные
        forecast_data = get_weather_data("forecast")

        if not forecast_data:
            await callback.message.answer(
                "❌ Не удалось получить прогноз",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Извлекаем нужный период
        hourly_data = calculate_hourly_data(forecast_data, "forecast", "now")

        if not hourly_data:
            await callback.message.answer(
                "❌ Нет данных за указанный период",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Форматируем и отправляем
        report = format_hourly_data(hourly_data, "next24h")

        await callback.message.answer(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()


@weather_router.callback_query(lambda c: c.data == "forecast_tomorrow")
async def forecast_tomorrow(callback: CallbackQuery):
    """Прогноз на завтра (только агрегированные данные)"""

    try:
        # Получаем данные
        forecast_data = get_weather_data("forecast")

        if not forecast_data:
            await callback.message.answer(
                "❌ Не удалось получить прогноз",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Извлекаем нужный период
        hourly_data = calculate_hourly_data(forecast_data, "forecast", "now")

        if not hourly_data:
            await callback.message.answer(
                "❌ Нет данных за указанный период",
                reply_markup=get_keyboard()
            )
            await callback.answer()
            return

        # Форматируем только агрегированные данные
        report = format_summary_report(hourly_data, "next24h")

        await callback.message.answer(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка: {e}",
            reply_markup=get_keyboard()
        )

    await callback.answer()