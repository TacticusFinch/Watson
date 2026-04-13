import asyncio
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import message
from dotenv import find_dotenv, load_dotenv

from bot import dp
from bot_instance import bot
from handlers.callbacks import cb

load_dotenv(find_dotenv())

from handlers.user_private import user_private_router, init_db, schedule_daily_tests
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message, edited_message']

dp.include_router(user_private_router)
dp.include_router(cb)

logging.basicConfig(
    level=logging.INFO,  # Или DEBUG, ERROR и т.д.
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',  # Или оставьте None для вывода в stdout
    filemode='a'
)


async def main():

    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    await init_db()  # Инициализация базы данных перед запуском пуллинга
    print("База данных инициализирована!")

    schedule_daily_tests(bot=bot)  # Запуск планировщика
    print("Планировщик запущен!")

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)  # Запуск пуллинга


if __name__ == '__main__':
    asyncio.run(main())