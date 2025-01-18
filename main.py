import asyncio
import os
from aiogram import Bot, types, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv

from bot_instance import bot
from handlers.admin_private import setup_scheduler
from handlers.callbacks import cb
from news import news_task, test_news, test_bot

load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private
from databases.questions_db import create_database
from databases.questions_db import insert_questions

ALLOWED_UPDATES = ['message, edited_message']

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(cb)
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
asyncio.run(main())