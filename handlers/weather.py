from aiogram import Router, types, F
from aiogram.types import CallbackQuery

from datetime import datetime, timedelta

import sys
sys.path.append(".")
from tools.getter import get_weather_data
from tools.status_calculate import calculate_daily_stats
from tools.report_formatter import format_weather_report
from tools.report_generator import generate_report_files
from tools.keyboard import get_keyboard

weather_router = Router()


@weather_router.callback_query(F.data == "report_daily")
async def report_daily(callback: CallbackQuery):
    """Погода за последние завершённые сутки (с 20:00 до 20:00)"""
    sent_message = await callback.message.answer("🔍 Получаю данные о погоде...")

    now = datetime.now()
    today_20 = now.replace(hour=20, minute=0, second=0, microsecond=0)

    # ВСЕГДА берём последние завершённые сутки (с 20:00 до 20:00)
    if now < today_20:
        # Если сейчас меньше 20:00, берём позавчера 20:00 -> вчера 20:00
        period_end = today_20 - timedelta(days=1)  # вчера 20:00
        period_start = period_end - timedelta(days=1)  # позавчера 20:00
        report_date = period_end  # дата отчёта = вчера
    else:
        # Если сейчас больше или равно 20:00, берём вчера 20:00 -> сегодня 20:00
        period_end = today_20  # сегодня 20:00
        period_start = today_20 - timedelta(days=1)  # вчера 20:00
        report_date = period_end  # дата отчёта = сегодня

    weather_data = get_weather_data(period_start, period_end)
    if weather_data:
        stats = calculate_daily_stats(weather_data, report_date)
        report = format_weather_report(stats)
        await sent_message.delete()
        await callback.message.answer(
            report,
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )
    else:
        await callback.message.answer(
            "❌ Не удалось получить данные о погоде.",
            reply_markup=get_keyboard()
        )

    await callback.answer()





@weather_router.callback_query(lambda c: c.data == "report_monthly")
async def report_monthly(callback: CallbackQuery):
    """Отчет за прошлый месяц в Excel и PDF"""
    sent_message = await callback.message.answer("📅 Генерирую отчет за прошлый месяц...")

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

        await sent_message.delete()
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
    sent_message = await callback.message.answer("📊 Генерирую отчет за прошлый квартал...")

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

        await sent_message.delete()
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
    sent_message = await callback.message.answer("📈 Генерирую отчет за прошлый год...")

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

        await sent_message.delete()
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