import asyncio
import json

from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, PollAnswer
from bot_instance import bot
from handlers.user_private import get_random_gem, final_test_results, user_states, polls, user_scores, send_test, \
    final_endgame_diagnostics_test_results, All_tests, welcome_prophet_test, start_fsm_test, Defenders
from keyboards.inline import tactic_tests, strategic_tests, prophet_levels, hard_prophet, \
    winordraw_tests, medium_prophet_3, medium_prophet, easy_prophet_perspectives, easy_prophet_opponent_vision, \
    easy_prophet_my_vision, medium_prophet_5, medium_prophet_4

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

@cb.callback_query(lambda c: c.data == 'endgame_diagnostics_results')
async def endgame_diagnostics_button(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await final_endgame_diagnostics_test_results(user_id,chat_id)


@cb.callback_query(lambda c: c.data == 'ninja')
async def ninja_test_button(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await send_test(chat_id, user_id, test_file=All_tests, test_name='ninja')


@cb.callback_query(lambda c: c.data == 'prophet_levels')
async def prophet_test_button(callback_query: CallbackQuery):
    await callback_query.message.answer("Выберите сложность", reply_markup=prophet_levels)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()


@cb.callback_query(lambda c: c.data == 'easy_prophet')
async def prophet_test_button(callback_query: CallbackQuery):
    await callback_query.message.answer("Выберите перспективу", reply_markup=easy_prophet_perspectives)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()

@cb.callback_query(lambda c: c.data == 'easy_prophet_my_vision')
async def prophet_test_button(callback_query: CallbackQuery):
    await callback_query.message.answer("Выберите номер теста", reply_markup=easy_prophet_my_vision)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()
@cb.callback_query(lambda c: c.data == 'easy_prophet_opponent_vision')
async def prophet_test_button(callback_query: CallbackQuery):
    await callback_query.message.answer('"Непобедим не тот, кто видит все пути к победе, а тот кто видит все пути к поражению".\n\nВ этих задачах ты должен найти победу за соперника.')
    await asyncio.sleep(2)
    await callback_query.message.answer("Выберите номер теста", reply_markup=easy_prophet_opponent_vision)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()

@cb.callback_query(lambda c: c.data == 'easy_prophet1')
async def prophet_1_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_1")


@cb.callback_query(lambda c: c.data == 'easy_prophet2')
async def prophet_2_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_2")

@cb.callback_query(lambda c: c.data == 'easy_prophet3')
async def prophet_3_button(callback_query: CallbackQuery, state: FSMContext):
        await welcome_prophet_test(callback_query.message, state, "easy_prophet_3")

@cb.callback_query(lambda c: c.data == 'easy_prophet4')
async def prophet_4_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_4")


@cb.callback_query(lambda c: c.data == 'easy_prophet5')
async def prophet_5_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_5")


@cb.callback_query(lambda c: c.data == 'easy_prophet6')
async def prophet_6_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_6")

@cb.callback_query(lambda c: c.data == 'easy_prophet7')
async def prophet_7_button(callback_query: CallbackQuery, state: FSMContext):
        await welcome_prophet_test(callback_query.message, state, "easy_prophet_7")

@cb.callback_query(lambda c: c.data == 'easy_prophet8')
async def prophet_8_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_8")

@cb.callback_query(lambda c: c.data == 'easy_prophet9')
async def prophet_9_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "easy_prophet_9")





@cb.callback_query(lambda c: c.data == 'medium_prophet')
async def medium_prophet_button(callback_query: CallbackQuery):
    await callback_query.message.answer("Выберите количество ходов в уме", reply_markup=medium_prophet)


@cb.callback_query(lambda c: c.data == 'medium_prophet_3')
async def prophet_test_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выберите номер теста", reply_markup=medium_prophet_3)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()

@cb.callback_query(lambda c: c.data == 'medium_prophet_4')
async def prophet_test_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выберите номер теста", reply_markup=medium_prophet_4)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()

@cb.callback_query(lambda c: c.data == 'medium_prophet_5')
async def prophet_test_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выберите номер теста", reply_markup=medium_prophet_5)

    # Не забываем "ответить" на callback_query, чтобы убрать "часики"
    await callback_query.answer()

@cb.callback_query(lambda c: c.data == 'hard_prophet')
async def prophet_1_button(callback_query: CallbackQuery):
    await callback_query.message.answer("Выберите количество ходов в уме", reply_markup=hard_prophet)

@cb.callback_query(lambda c: c.data == 'hard_prophet8')
async def prophet_1_button(callback_query: CallbackQuery, state: FSMContext):
    await welcome_prophet_test(callback_query.message, state, "hard_prophet8_1")

@cb.callback_query(lambda c: c.data == 'winordraw')
async def winordraw_button(callback_query: CallbackQuery):
        await callback_query.message.answer("Выберите номер теста", reply_markup=winordraw_tests)


@cb.callback_query(lambda c: c.data == 'winordraw1')
async def winordraw_button1(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await send_test(chat_id, user_id, test_file=All_tests, test_name='winordraw1')

@cb.callback_query(lambda c: c.data == 'winordraw2')
async def winordraw_button2(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await send_test(chat_id, user_id, test_file=All_tests, test_name='winordraw2')

@cb.callback_query(lambda c: c.data == 'winordraw3')
async def winordraw_button3(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await send_test(chat_id, user_id, test_file=All_tests, test_name='winordraw3')


@cb.callback_query(lambda c: c.data == 'defend')
async def defend_button3(callback_query: CallbackQuery):
    await callback_query.message.answer("Выбери тему", reply_markup='defend')

@cb.callback_query(lambda c: c.data == 'defenders')
async def defenders_button(callback_query: CallbackQuery, state: FSMContext):
    await start_fsm_test(callback_query.message, state, "defenders", Defenders)

@cb.callback_query(lambda c: c.data == 'theoretic')
async def winordraw_button3(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await send_test(chat_id, user_id, test_file=All_tests, test_name='endgame_diagnostics')


# @cb.callback_query(lambda c: c.data == 'openstore')
# async def openstorebutton(callback_query: CallbackQuery):




# @cb.callback_query(lambda c: c.data == 'white')
# async def white(callback_query: CallbackQuery, state: FSMContext):
#     chat_id = callback_query.message.chat.id
#
#
#
# @cb.callback_query(lambda c: c.data == 'black')
# async def black(callback_query: CallbackQuery, state: FSMContext):