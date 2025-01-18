import asyncio

from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, PollAnswer
from bot_instance import bot
from handlers.user_private import get_random_gem, final_test_results, user_states, polls, ninja_questions, user_scores
from keyboards.inline import tactic_tests, strategic_tests

cb = Router()

@cb.callback_query(lambda c: c.data == 'tactic')

async def tactic_pressed_button(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text="Выберите тему: ", reply_markup=tactic_tests)

async def strategy_pressed_button(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text="Выберите тему: ", reply_markup=strategic_tests)

@cb.callback_query(lambda c: c.data == 'next')
async def next_pressed_button(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await get_random_gem(callback_query.message, state)

@cb.callback_query(lambda c: c.data == 'might_results')
async def next_pressed_button(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    await final_test_results(user_id)