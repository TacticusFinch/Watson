from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from apscheduler.triggers.date import DateTrigger

from bot_instance import bot

scheduler = AsyncIOScheduler()
async def send_reminder(chat_id):
    await bot.send_message(chat_id, text="Укусите Анечку, сэр")
# Настройка планировщика
def setup_scheduler(chat_id):
    # Добавляем задачу в планировщик, передавая `bot` как аргумент через `kwargs`
    scheduler.add_job(
        func=send_reminder,        # Передаём функцию
        kwargs={"chat_id": chat_id},  # Передача аргументов функции
        trigger=DateTrigger(run_date=datetime(2024, 12, 20, 3, 7)),
        id="reminder_task"
    )

    scheduler.start()
    # Запуск планировщика

