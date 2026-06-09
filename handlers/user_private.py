import asyncio
import json
import logging
import os
import random
import re
import sqlite3
import requests
import aiosqlite

from collections import defaultdict
from aiogram import types, Bot, Router, Dispatcher
from aiogram.enums import ParseMode, MessageEntityType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile, PollAnswer, MessageEntity
from aiogram.filters.state import StateFilter
from aiogram.types.web_app_info import WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime

from apscheduler.triggers.cron import CronTrigger

from bot import dp
#from sqlalchemy.dialects.sqlite import aiosqlite

from bot_instance import bot
from databases.facts_db import insert_facts_from_list
from keyboards.inline import tactic_tests, strategic_tests, next_button, test_might_results, endgame_diagnostics_results
from keyboards.reply import tactic_strategy_button
from collections import defaultdict

polls = defaultdict(dict)

MEMES_FOLDER = "memes"
PUZZLE_FOLDER = "puzzles"
BRILLIANTS_FOLDER = "brilliants"
CHAT_ID = None


OPENROUTER_API_KEY ="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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

scheduler = AsyncIOScheduler()
user_level_3_ids = [2119353166, 1139034211, 7877529350, 7877529350, 7777781328, 6091002843, 5255725303, 1186939115, 5276190685, 6804661582, 6668604221, 6126719516, 5828167970, 6283356137, 6662455423, 2097858255, 7698243378, 6672279908, 6601893986, 6209517485, 6032405861, 6113872493, 5776038271, 6710467312]
my_ids = [2119353166]
user_level_1_ids = [2119353166]#, 2119353166, 6627798006, 7294169822, 6356510135, 5879786452, 7968414403, 7394276254, 7740277351, 6483117741, 6283614567, 984742231, 1451398913, 5569265124, 6934691008, 5977196372, 5534205178, 7450839606, 771827523, 6528529601, 7331880668, 6593272248, 7876684402]
all_users_ids = [2119353166, 1186939115, 5276190685, 6804661582, 6668604221, 6126719516, 5828167970, 6283356137, 6662455423, 2097858255, 7698243378, 6672279908, 6601893986, 6209517485, 6032405861, 6113872493, 5776038271, 6710467312, 750941958, 2119353166, 6627798006, 7294169822, 6356510135, 5879786452, 7968414403, 7394276254, 7740277351, 6483117741, 6283614567, 984742231, 1451398913, 5569265124, 6934691008, 5977196372, 5534205178, 7450839606, 771827523, 6528529601, 7331880668, 6593272248, 7876684402]
DB_PATH = "databases/chat_log.db"
misquestions = {}
knowledge_base = {
    "Кто такой архитектор?": "Это создатель нашей матрицы!"
}


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к БД: {e}")
    return conn

def insert_user_results(conn, user_name, test_name, score, misquestions):
    try:
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO user_results (user_name, test_name, score, misquestions)
                VALUES (?, ?, ?, ?)
            """, (user_name, test_name, score, misquestions))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при вставке данных: {e}")


conn = create_connection("databases/chat_log.db")
def retrieve_info(query):
    return knowledge_base.get(query.lower(), "Я не знаю этого, но могу попробовать объяснить.")



user_histories = {}
def ask_chess_guru(user_id, question):

    if user_id not in user_histories:
        user_histories[user_id] = [
            {"role": "system", "content": "Тебя зовут Тактикус. Ты - шахматный помощник, созданный Жамсо Валерьевичем для помощи в подготовке будущих чемпионов стран и мира. Помоги пользователю с вопросами, касающимися шахмат"}
        ]
    user_histories[user_id].append({"role": "user", "content": question})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "nvidia/nemotron-3-super-120b-a12b:free",  # Указываем модель шахматного тренера
        "messages": user_histories[user_id],
        "max_tokens": 2000,
        "temperature": 0.4,
    }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        logging.info(f"HTTP статус ответа: {response.status_code}")

        # Если сервер вернул ненормальный статус
        if response.status_code != 200:
            logging.error(f"Некорректный статус ответа: {response.status_code}. Ответ от сервера: {response.text}")
            return f"Ошибка: сервер вернул код {response.status_code}. Проверяйте данные запроса."
        if response.status_code == 401:
            return "Ошибка авторизации. Проверьте API-ключ."
        elif response.status_code == 429:
            return "Превышен лимит запросов. Попробуйте позже."
        elif response.status_code >= 500:
            return "Сервис временно недоступен. Попробуйте позже."

        response.raise_for_status()  # Проверяет успешность запроса
        result = response.json()
        print(result)
        assistant_reply = result["choices"][0]["message"]["content"]

        # Добавляем ответ ассистента в историю
        user_histories[user_id].append({"role": "assistant", "content": assistant_reply})
        if len(user_histories[user_id]) > 30:
            user_histories[user_id] = user_histories[user_id][-30:]

        return assistant_reply

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка в запросе: {e}")
        return "Произошла ошибка сети. Попробуйте позже."
    except json.JSONDecodeError:
        logging.error(f"Ответ не JSON: {response.text}")
        return "Ошибка обработки ответа от сервера. Пожалуйста, попробуйте ещё раз позже."

global test_index
test_index = 3

global test_prophet_index
test_prophet_index = 0

dialogues = {}
MAX_HISTORY_LENGTH = 3000  # Максимальная длина истории в символах

def trim_history(history):
    text = "".join(msg["message"] for msg in history)
    if len(text) > MAX_HISTORY_LENGTH:
        # Сохранить только последние сообщения
        history = history[-5:]  # Оставить последние 5 сообщений
    return history
def add_message_to_history(user_id, message, sender="user"):
    if user_id not in dialogues:
        dialogues[user_id] = []
    dialogues[user_id].append({"sender": sender, "message": message})
    dialogues[user_id] = trim_history(dialogues[user_id])

def get_history(user_id):
    return dialogues.get(user_id, [])
    # Сокращаем историю, если нужно

user_private_router = Router()

with open("All_tests.json", "r", encoding="utf-8") as f:
    All_tests = json.load(f)

with open("Prophets.json", "r", encoding="utf-8") as f:
    Prophets = json.load(f)

with open("Defenders.json", "r", encoding="utf-8") as f:
    Defenders = json.load(f)

CURRENT_TEST_FILE = "current_test.json"


user_states = {
    'might': {},
    'style': {},
    'ninja': {},
    'checks': {},
    'captures': {},
    'gifts': {},
    'mate_in_1': {},
    'mate2': {},
    'trap?': {},
    'yesno': {},
    'openning': {},
    'prophet': {},
    'easy_prophet_1': {},
    'easy_prophet_2': {},
    'easy_prophet_3': {},
    'easy_prophet_4': {},
    'easy_prophet_5': {},
    'easy_prophet_6': {},
    'easy_prophet_7': {},
    'easy_prophet_8': {},
    'easy_prophet_9': {},
    'easy_prophet_10': {},
    'easy_prophet_11': {},
    'easy_prophet_12': {},
'easy_prophet_13': {},
'easy_prophet_14': {},
'easy_prophet_15': {},
'easy_prophet_16': {},
'easy_prophet_17': {},
    'medium_prophet1': {},
    'hard_prophet8_1': {},
    'winordraw1': {},
    'winordraw2': {},
    'winordraw3': {},
    'endgame_diagbostics': {},
    'defenders': {}

}

polls = {
    'might': {},
    'style': {},
    'ninja': {},
    'checks': {},
    'captures': {},
    'gifts': {},
    'mate_in_1': {},
    'mate2': {},
    'trap?': {},
    'yesno': {},
    'openning': {},
    'prophet': {},
    'endgame_diagnostics': {},
    'winordraw1': {},
    'winordraw2': {},
    'winordraw3': {},
}

user_scores = defaultdict(int)
@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Давай посмотрим, что я могу тебе предложить 😉\n\n'
                         "🔹 Заполнить анкету\n"
                         "🔹 Режим гуру\n"
                         "🔹 Конкурс решения задач!\n"
                         "🔹 Магазин\n"
                         "🔹 Тест силы\n"
                         "🔹 Диагностика стиля игры. (в разработке)\n"
                         "🔹 Нестандартные тренажеры (в разработке)\n"
                         "🔹 Шутку (мем)\n"
                         "🔹 Рассказать мудрость\n"
                         "🔹 Рассказать интересный факт\n\n"
                          "🛠 Для начала работы нажмите кнопку ниже или используйте меню\n\n"
                         "/start - перезапустить бота\n"
                         "/guru - расскажу всё о шахматах\n"
                         "/challenge - конкурс решения задач!\n"
                         "/store - лавка Тактикуса\n"
                         "/bio - заполнить анкету\n"
                         "/wish - расскажи, что хочешь видеть в лавке\n"
                         "/test - тест силы\n"
                         "/quiz - случайный тест\n"
                         "/style - найти свой стиль\n"
                         "/meme - шахматный мем\n"
                         "/train - тренажеры тактики и стратегии\n"
                         "/mem4gem - мемас за алмаз\n"
                         "/pearl - мудрость\n"
                         "/fact - интересный факт\n"
                         )
user_bio_states = {}
bio_questions = [
    {
        "question": "Вопрос 1. Как тебя зовут? (Напиши имя, фамилию, отчество)",
        "image_path": "style/eleven.png"
    },
    {
        "question": "Вопрос 2. Какая у тебя дата рождения?",
        "image_path": "style/birthday.jpg"
    },
    {
        "question": "Вопрос 3. Какое твоё самое любимое блюдо?",
        "image_path": "style/ramen.jpg"
    },
    {
        "question": "Вопрос 4. Кто твой самый любимый герой? Можешь назвать любого персонажа из книги, мультфильма или игры.",
        "image_path": "style/favourcharacter.jpg"
    },
    {
        "question": "Вопрос 5. Какое твоё самое любимое занятие в свободное время?",
        "image_path": "style/freetime.jpg"
    },
    {
        "question": "Вопрос 6. Кем ты мечтаешь стать, когда вырастешь?",
        "image_path": "style/jobs.jpg"
    },
    {
        "question": "Вопрос 7. Есть ли у тебя любимая книга или фильм? Напиши названия.",
        "image_path": "style/book.jpg"
    },
    {
        "question": "Вопрос 8. Если бы у тебя было своё изобретение, что бы ты придумал(а)?",
        "image_path": "style/invention.jpg"
    },
    {
        "question": "Вопрос 9. Какое твоё самое необычное или неожиданное умение?",
        "image_path": "style/catguitar.jpg"
    },
    {
        "question": "Вопрос 10. Есть ли что-то, что ты хотел(а) бы рассказать, но о чём тебя обычно не спрашивают?",
        "image_path": "style/ufo.jpg"
    },


]
#     "Вопрос 2. Какая у тебя дата рождения?",
#     "Вопрос 3. Какое твоё самое любимое блюдо?",
#     "Вопрос 4. Кто твой любимый персонаж? Можешь назвать персонажа из книги, мультфильма или игры.",
#     "Вопрос 5. Какое твоё самое любимое занятие в свободное время?",
#     "Вопрос 6. Кем ты мечтаешь стать, когда вырастешь?",
#     "Вопрос 7. Какое твоё самое необычное или неожиданное умение?",
#     "Вопрос 8. Чему бы ты очень хотел(а) научиться?",
#     "Вопрос 9. Есть ли у тебя любимая книга или фильм? Напиши названия.",
#     "Вопрос 10. Если бы у тебя была возможность путешествовать в любую страну, куда бы ты отправился/отправилась?",
#     "Вопрос 11. Если бы у тебя было своё изобретение, что бы ты придумал(а)?",
#     "Вопрос 12. Какой школьный предмет тебе больше всего нравится и почему?",
#     "Вопрос 13. Придумай название и девиз для команды, в которой ты бы хотел(а) участвовать",
#     "Вопрос 14. Если бы ты был супергероем, как бы тебя звали",
#     "Вопрос 15. Какой один совет ты дал бы учителям, чтобы уроки были увлекательнее?",
#     "Вопрос 16. Есть ли что-то, что ты хотел бы рассказать, но о чём тебя обычно не спрашивают?",
#     "Вопрос 17. Хотел(а) бы ты, чтобы твои ответы на анкету увидели другие участники?",
# ]

mem4gem_questions = [
    {
        "image_path": "brilliants/1.png",
        "correct": "Qf5"
    },
    {
        "image_path": "brilliants/2.png",
        "correct": "Qh6"
    },
    {
        "image_path": "brilliants/3.png",
        "correct": "F5"
    },
    {
        "image_path": "brilliants/4.png",
        "correct": "Rd7"
    },
    {
        "image_path": "brilliants/5.png",
        "correct": "Rd7"
    },
    {
        "image_path": "brilliants/6.png",
        "correct": "Re4"
    },
    {
        "image_path": "brilliants/7.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/8.png",
        "correct": "Nd7"
    },
    {
        "image_path": "brilliants/9.png",
        "correct": "Nf6"
    },
    {
        "image_path": "brilliants/10.png",
        "correct": "Nf6"
    },
    {
        "image_path": "brilliants/11.png",
        "correct": "Ra8"
    },
    {
        "image_path": "brilliants/12.png",
        "correct": "Rh8"
    },
    {
        "image_path": "brilliants/13.png",
        "correct": "Re6"
    },
    {
        "image_path": "brilliants/14.png",
        "correct": "Ra8"
    },
    {
        "image_path": "brilliants/15.png",
        "correct": "Be3"
    },
    {
        "image_path": "brilliants/16.png",
        "correct": "Bf7"
    },
    {
        "image_path": "brilliants/17.png",
        "correct": "Qg7"
    },
    {
        "image_path": "brilliants/18.png",
        "correct": "Qg1"
    },
    {
        "image_path": "brilliants/19.png",
        "correct": "Qg8"
    },
    {
        "image_path": "brilliants/20.png",
        "correct": "Qg8"
    },
    {
        "image_path": "brilliants/21.png",
        "correct": "Ng6"
    },
    {
        "image_path": "brilliants/22.png",
        "correct": "Qf7"
    },
    {
        "image_path": "brilliants/23.png",
        "correct": "Qc6"
    },
    {
        "image_path": "brilliants/24.png",
        "correct": "Rc6"
    },
    {
        "image_path": "brilliants/25.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/26.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/27.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/28.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/29.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/30png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/31.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/32.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/33.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/34.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/35.png",
        "correct": "Bd6"
    },
    {
        "image_path": "brilliants/36.png",
        "correct": "Bd6"
    },

]

pearls = [
    "Победа достается тому, кто сделал ошибку предпоследним.divСавелий Тартаковер",
    "Вы можете узнать гораздо больше из проигранной игры, чем от выигранной. Вы должны проиграть сотни игр, прежде чем стать хорошим игроком.divХосе Рауль Капабланка, 3-ий чемпион мира",
    "Не ход ищи, не два хода, а целый план ищи.divЗноско-Боровский",
    "Твоя игра не может быть лучше, чем твой худший ход.divДэн Хейсма",
    "Первый принцип наступления: не позволяйте врагу развиваться.divРоберт Файн",
    "Если противник предлагает ничью, попытайся понять, почему он считает, что стоит хуже.divНайджел Шорт",
    "Один плохой ход может испортить сорок хороших.divГовард Хоровиц",
    "Шахматы, подобно музыке, или любому другому искусству, способны делать человека счастливым.divЗигберт Тарраш",
    "Слабости характера обычно проявляются во время шахматной партии.divГарри Каспаров",
    "В шахматах выигрывает каждый. Если ты получаешь удовольствие от игры, а это самое главное, то даже поражение не страшно.divДавид Бронштейн"
]

async def init_db():
    """ Инициализация базы данных """
    async with aiosqlite.connect("databases/users_homework.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id INTEGER PRIMARY KEY,
            hometest_index INTEGER DEFAULT 0,
            question_index INTEGER DEFAULT 0,
            username TEXT DEFAULT '',
            date TEXT DEFAULT ''
        )
        """)
        await db.commit()


async def get_user_progress(user_id):
    """ Получает текущий тест и номер вопроса пользователя """
    async with aiosqlite.connect("databases/users_homework.db") as db:
        cursor = await db.execute("SELECT hometest_index, question_index FROM user_progress WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row if row else (0, 0)


async def update_user_progress(user_id, hometest_index, question_index, username=None, date=None):
    """Обновляет прогресс пользователя, и при необходимости — имя и дату"""
    async with aiosqlite.connect("databases/users_homework.db") as db:
        # Получаем текущее значение, если не передано новое
        if username is None or date is None:
            cursor = await db.execute("SELECT username, date FROM user_progress WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            await cursor.close()
            if row:
                username = username or row[0]
                date = date or row[1]
            else:
                username = username or ''
                date = date or ''

        await db.execute("""
            INSERT INTO user_progress (user_id, hometest_index, question_index, username, date)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET 
                hometest_index = excluded.hometest_index,
                question_index = excluded.question_index,
                username = excluded.username,
                date = excluded.date
        """, (user_id, hometest_index, question_index, username, date))
        await db.commit()



def save_user_result(db_path: str, user_id: int, test_id: int, score: int) -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    passed_at = datetime.datetime.now().isoformat(timespec='seconds')
    cursor.execute(
        "INSERT INTO user_results (user_id, test_id, score, passed_at) VALUES (?, ?, ?, ?)",
        (user_id, test_id, score, passed_at)
    )
    result_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return result_id
class CheckState(StatesGroup):
    waiting_for_answer = State()


@user_private_router.message(Command('test'))
async def test_your_might(message: types.Message):
    await message.answer(
        "Это тест на определение уровня игры. Он нужен нам для определения твоих слабых сторон. В каждой задаче ты играешь нижними фигурами. Поехали!")
    await asyncio.sleep(2)
    await start_test(message)


async def start_test(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states['might'][user_id] = 0
    user_scores[user_id] = 0
    await send_test(chat_id, user_id, test_file=All_tests, test_name='might')

async def send_test(chat_id, user_id, test_file, test_name):
    # Получаем вопросы для теста
    test = next((test_obj for test_obj in test_file if test_obj["id"] == test_name), None)
    # Извлечем вопросы из теста
    questions = test["questions"] if test else []
    user_states.setdefault(test_name, {}).setdefault(user_id, 0)
    current_question_index = user_states[test_name][user_id]
    # Если есть вопросы, отправляем следующий
    if current_question_index < len(questions):
        question_data = questions[current_question_index]
        image_file = FSInputFile(question_data["image_path"])
        await bot.send_photo(chat_id, photo=image_file)

        if test_name != 'style':
            if not question_data.get("question"):
                # Если вопрос отсутствует или пустой — пропускаем этот пункт и переходим к следующему
                return  # или continue, если внутри цикла
            poll = await bot.send_poll(
            chat_id=chat_id,
            question=question_data["question"],
            options=question_data["options"],
            type="quiz",
            correct_option_id=question_data["correct"],
            is_anonymous=False
         )
        else:
            poll = await bot.send_poll(
                chat_id=chat_id,
                question=question_data["question"],
                options=question_data["options"],
                type="regular",
                is_anonymous=False
            )

        polls[test_name][poll.poll.id] = user_id
@user_private_router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    # Найти user_id по poll_id, связав его с одним из тестов
    user_id, test_name = None, None
    for name in ['might', 'style', 'ninja', 'checks', 'captures', 'gifts', 'mate_in_1', 'endgame_diagnostics', 'winordraw1']:
        user_id = polls[name].get(poll_answer.poll_id)
        if user_id:
            test_name = name
            break

    # Если пользователь не найден для текущего poll_id, завершить обработку
    if not user_id:
        await bot.send_message(chat_id=poll_answer.user.id, text='Тест не найден.')
        return

    hometest_index, question_index = await get_user_progress(user_id)
    print(hometest_index, question_index)
    # Получить текущий индекс вопроса для пользователя
    current_question_index = user_states[test_name].get(user_id, 0)
    next_question_index = question_index + 1

    # Найти тест в списке All_tests
    test = next((test_obj for test_obj in All_tests if test_obj["id"] == test_name), None)
    questions = test["questions"] if test else []

    # Проверить, правильный ли ответ был дан
    user_response = poll_answer.option_ids
    if user_response[0] == questions[question_index]['correct']:
        user_scores[user_id] = user_scores.get(user_id, 0) + 1
    else:
        # Если ответ неправильный — сохраняем вопрос в misquestions
        # Убедимся, что для user_id есть список, куда мы складываем ошибки:
        if user_id not in misquestions:
            misquestions[user_id] = {}
        if test_name not in misquestions[user_id]:
            misquestions[user_id][test_name] = []

        misquestions[user_id][test_name].append(question_index+1)
        # Если ещё есть вопросы — отправить следующий, иначе завершить тест
    if next_question_index < len(questions):
        user_states[test_name][user_id] = next_question_index  # Обновляем индекс
        question_index += 1
        await update_user_progress(user_id, hometest_index, question_index)
        #await send_next_homework_question_for_beginners(user_id, bot)
        await send_test(chat_id=poll_answer.user.id, user_id=user_id, test_file=All_tests, test_name=test_name)
    else:
        # Завершение теста
        user_states[test_name].pop(user_id, None)
        polls[test_name].pop(poll_answer.poll_id, None)
        user_name = poll_answer.user.first_name
        misquestions_str = " ".join(
            map(str,
                misquestions.get(user_id, {}).get(test_name, []))
        )
        insert_user_results(conn, user_name, test_name, user_scores[user_id], misquestions_str)
        await test_results(user_id, test_name, user_scores)
        hometest_index +=1
        question_index=0
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update_user_progress(user_id, hometest_index, question_index, user_name, date)

async def test_results(user_id, test_name, user_scores):
    if test_name == 'might':
        await bot.send_message(
            chat_id=user_id,
            text=f"🎉 Тест завершен! Данные получены.",
            reply_markup=test_might_results
        )
    elif test_name == 'endgame_diagnostics':
        await bot.send_message(
            chat_id=user_id,
            text=f"🎉 Тест завершен! Данные получены.",
            reply_markup=endgame_diagnostics_results
        )
    else:
        if 10 <= user_scores[user_id] <= 12:
            gradepic = "grades/5.png"
            grade_text = "Оценка - 5. Результат фантастический! А вы случайно не читер?"
            photopic = FSInputFile(gradepic)
        elif 8 <= user_scores[user_id] < 10:
            gradepic = "grades/4.png"
            grade_text = "Оценка - 4. Тебя можно поздравить! Хорошо!"
            photopic = FSInputFile(gradepic)
        elif 5 <= user_scores[user_id] <= 7:
            gradepic = "grades/3.png"
            grade_text = "Оценка - 3. Зато не двойка!"
            photopic = FSInputFile(gradepic)
        elif 0 <= user_scores[user_id] < 5:
            gradepic = "grades/2.png"
            grade_text = "Оценка - 2. Думаю, ты способен на большее."
            photopic = FSInputFile(gradepic)

        await bot.send_message( chat_id=user_id,
                            text=f"🎉 Тест завершен! Количество баллов: {user_scores.get(user_id, 0)} из 12.",
                           )
        await bot.send_photo(chat_id=user_id, photo=photopic)
        await bot.send_message(chat_id=user_id, text=grade_text)
    #     await bot.send_message(user_id, "🕺", entities=[MessageEntity(
    #         type=MessageEntityType.CUSTOM_EMOJI,
    #         offset=0,
    #         length=1,
    #         custom_emoji_id="5465321651954526991"
    #     )
    # ])
        await bot.send_message(user_id, "Независимо от результата, ты стал лучше 👏\n\nУвидимся в следующем тесте 😉")

async def final_test_results(user_id):
    chat_id = user_id
    if 0 < user_scores[user_id] <= 5:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/pawn.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Пешка.\nКоличество правильных ответов: {user_scores[user_id]} из 25. \nУровень игры на Lichess - 800-1000. ")
    elif 5 < user_scores[user_id] <= 10:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/knight.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Конь.\nКоличество правильных ответов: {user_scores[user_id]} из 25. \nУровень игры на Lichess - 1100-1200.")
    elif 10 < user_scores[user_id] <= 15:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/bishop.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Слон.\nКоличество правильных ответов: {user_scores[user_id]} из 25. \nУровень игры на Lichess - 1300-1400.")
    elif 15 < user_scores[user_id] <= 18:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/rook.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Ладья.\nКоличество правильных ответов: {user_scores[user_id]} из 25. \nНеплохо. Уровень игры на Lichess - 1400-1500.")
    elif 18 < user_scores[user_id] <= 20:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/crazy-rook.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Бешеная Ладья.\n Количество правильных ответов: {user_scores[user_id]} из 25. \nВесьма неплохо. Уровень игры на Lichess - 1600-1700.")
    elif 20 < user_scores[user_id] <= 22:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/queen.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Ферзь. \nКоличество правильных ответов: {user_scores[user_id]} из 25. \nХороший результат! Уровень игры на Lichess - 1800-1900.")
    else:
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("final_test_pics/king.jpg"))
        await bot.send_message(chat_id=chat_id, text=f"Ранг: Король.\nКоличество правильных ответов: {user_scores[user_id]} из 25.\nВеликолепный результат! У вас отличное тактическое зрение и хороший уровень позиционной игры. Уровень игры на Lichess: 2000+")

async def final_endgame_diagnostics_test_results(user_id, chat_id):
    await bot.send_message(chat_id, text=f"Твой результат: {user_scores[user_id]} из 48.\nПодведение итогов и выявление победителя будет в воскресенье перед онлайн-турниром.\n\nСпасибо за участие! 🥳")



@user_private_router.message(Command('style'))
async def send_welcome_style(message: types.Message):
    await message.answer("Это тест на определение твоего стиля игры. Кто ты: ассасин, волшебник или вяленая рыба?")
    await asyncio.sleep(2)
    await start_style_test(message)


async def start_style_test(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states['style'][user_id] = 0
    await send_test(chat_id, user_id, test_file=All_tests, test_name='style')


@user_private_router.message(Command('ninja'))
async def send_welcome_ninja(message: types.Message):
    await message.answer("Это тест на избавление от зевков")
    await asyncio.sleep(2)
    await start_ninja_test(message)

async def start_ninja_test(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states['ninja'][user_id] = 0
    user_scores[user_id] = 0
    await send_test(chat_id, user_id, test_file=All_tests, test_name='ninja')

@user_private_router.message(Command('mem4gem'))
async def welcome_start_m4g(message: types.Message, state: FSMContext):
    await message.answer(
        "В каждой задаче найдите бриллиантовый ход 💎\nВводите ход вручную. \nЕсли решение правильное, будет показан шахматный мем.\nОсобое внимание удели обозначениям, это важно:")
    chat_id = message.chat.id
    notation_image = FSInputFile("brilliants/Notation.png")
    await bot.send_photo(chat_id, photo=notation_image)
    await message.answer("Начнём!")
    await asyncio.sleep(2)
    await start_m4g_test(message, state)

async def start_m4g_test(message: types.Message, state: FSMContext):
    print("Запустим проверку")
    await get_random_gem(message, state)

async def get_random_gem(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    random_gem = random.choice(mem4gem_questions)
    print(random_gem)
    await bot.send_photo(chat_id, photo=FSInputFile(random_gem["image_path"]))
    await state.update_data(random_gem=random_gem)
    await state.set_state(CheckState.waiting_for_answer)

@user_private_router.message(StateFilter(CheckState.waiting_for_answer))
async def check_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    random_gem = user_data.get('random_gem')
    user_answer = message.text
    if user_answer.lower() == random_gem["correct"].lower():
        await message.answer("Молодец!")
        await send_meme(message)
        await message.answer("Еще?", reply_markup=next_button)
        await state.clear()
    else:
        if user_answer[0] != '/':
            await message.answer("Неправильно. Попробуй снова!\nИли нажми кнопку ниже.", reply_markup=next_button)
        else:
            await state.clear()

@user_private_router.message(Command('train'))
async def send_welcome(message: types.Message):
    await message.answer("Выберите категорию\n", reply_markup=tactic_strategy_button)


@user_private_router.message(Command('puzzle'))
async def send_puzzle(message: types.Message):
    puzzle = FSInputFile(get_random_puzzle())
    await message.answer_photo(puzzle, "||Здесь должен быть ответ ||", parse_mode="MarkdownV2")


def get_random_puzzle():
    puzzles = os.listdir(BRILLIANTS_FOLDER)
    if not puzzles:
        return None
    random_puzzle = random.choice(puzzles)
    return os.path.join(BRILLIANTS_FOLDER, random_puzzle)


@user_private_router.message(Command('meme'))
async def send_meme(message: types.Message):
    meme = FSInputFile(get_random_meme())
    await message.answer_photo(meme)


def get_random_meme():
    memes = os.listdir(MEMES_FOLDER)
    if not memes:
        return None
    random_memes = random.choice(memes)
    return os.path.join(MEMES_FOLDER, random_memes)


@user_private_router.message(Command('pearl'))
async def send_pearl(message: types.Message):

    wisdom = random.choice(pearls)
    escaped_wisdom = escape_markdown_v2(wisdom)
    #italic_wisdom = f"_{escaped_wisdom}_"
    formatted_wisdom = format_wisdom(escaped_wisdom)
    await message.answer(formatted_wisdom, parse_mode='MarkdownV2')

def format_wisdom(wisdom):
    parts = wisdom.split("div")
    text = parts[0]
    author = parts[1] if len(parts) > 1 else " "
    formatted_wisdom = f'"_{text}_"\n\n{author}'
    return formatted_wisdom
def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2"""
    special_chars = r"([_*[\]()~`>#+\-=|{}.!])"
    return re.sub(special_chars, r"\\\1", text)

facts = [
    "Теоретически самая длинная партия может длиться максимум 5949 ходов.",
    "Прародительницей шахмат является Индия. Неудивительно, что в этом крае мудрости и особого взгляда на мир появилась эта прекрасная игра.",
    "Шахматы из Индии, эпоха государства Гуптов (около 1400 лет назад) попали в Эраншахр (территория современного Ирана и Ирака), затем на Ближний Восток, в Европу и Россию.",
    "В реальности самая длинная шахматная партия длилась 20 часов и 15 минут. Иван Николич и Горан Арсович сделали на двоих 269 ходов и сыграли вничью.",
    "Вторая книга в истории на английском языке была о шахматах (первая – сборник о Троянской войне).",
    "Кстати, бывали даже заочные битвы городов. Например, в XIX веке Лондон играл против Эдинбурга.",
    "Китайский император Вэнь-ди казнил двух шахматистов, когда узнал, что они называют ферзей императорами.",
    "В США не очень продуманный первый ход называют «атакой Рейгана».",
    "В среднем 37,5% партий на турнирах профессионалов выигрывают белые фигуры, 27,6% – черные. Остальные заканчиваются ничьей.",
    "В повести братьев Стругацких «Полдень, XXII век» упоминается метод «Каспаро-Карпова». В год издания повести (1962) Анатолию Карпову было 11 лет, а Гарри Каспаров еще не родился.",
    "До изобретения механических часов шахматисты использовали песочные.",
    "Немецкий шахматист Эмануил Ласкер 27 лет удерживал титул чемпиона мира.",
    "Если у шахматиста во время игры зазвонит телефон, то ему автоматически засчитают поражение или назначат ничью, если противник в теории не мог уже победить.",
    "У историков популярна версия, что Иван Грозный умер за игрой в шахматы.",
    "В 1970 году была сыграна шахматная партия «Космос-Земля». Летчики «Союза-9» играли с другими летчиками на Земле по радио.",
    "Складную шахматную доску изобрел священник в XII веке. Церковь запрещала ему играть в шахматы, поэтому он придумал такую хитрость, как будто две книги лежат вместе.",
    "Когда игроки делают по четыре хода, то дальше есть более 318 миллиардов вариантов, как закончится партия.",
    "В 2005 году в Рейкьявике на 14 тысяч жителей приходился один шахматный гроссмейстер.",
    "В Армении шахматы – школьный предмет.",
    "Первый «шахматный автомат» был изобретен в 1769 году, чтобы впечатлить австрийскую королеву. Но он оказался мистификацией: играл не «механический турок», а карлик, который сидел в коробке и управлял фигурами на магнитах.",
    "Суперкомпьютер Deep Blue дважды играл с Гарри Каспаровым – 1:1. А «Дисней» приобрела права на экранизацию пьесы по мотивам этого матча.",
    "Пушкин любил шахматы, и в «Евгении Онегине» есть строчки: «И Ленский пешкою ладью / Берет в рассеянье свою». На основе этого воссоздана целая партия Лариной и Ленского. ",
    "Во время игры в шахматы активизируются оба полушария мозга, улучшаются творческие способности, концентрация, навыки чтения и критическое мышление.",
    "Первое упоминание шахмат в Америке относится к 1641 году и связано с городом Эстер Синглтон, где в то время жили голландские поселенцы. А первый шахматный турнир в США состоялся в Нью-Йорке в 1857 году.",
    "Самый старый из сохранившихся наборов шахмат был найден на острове Льюис в Северной Шотландии. Он датируется XII веком нашей эры, и предположительно создан в Исландии или Норвегии. Его оригинальное исполнение послужило образцом для волшебных шахматных фигур в фильме «Гарри Поттер и философский камень».",
    "Число шахматных партий, которые шахматисты могут разыграть на доске, значительно превышает число атомов в доступной человечеству части вселенной.",
    "Длиннейшая серия последовательных шахов, которая была зарегистрирована, насчитывает 74. 15 – наибольшее число фигур, которые были захвачены противником на одной клетке. Данная клетка даже именовалась «черной дырой».",
    "Шахматы — это прекрасный способ улучшить память не только детей, но и пожилых. Игра по праву считается отличным средством в борьбе с болезнью Альцгеймера.",
    "Каждый начинающий шахматист знает, что пешка, которая начинает игру, может пойти не только на одну, но и на две клетки вперед. Но это правило появилось не сразу, а в 1280 году в Испании.",
    "Шахматный термин «гамбит» произошел от итальянского выражения «dare il gambetto»—«ставить подножку».",
    "Самый долгий по времени ход принадлежит бразильцу Франсиско Троису: на его обдумывание шахматист потратил два часа и двадцать минут.",
    "В шахматы можно играть и без съедения фигур. Известна партия, которая игралась без съедения фигур на протяжении 94 ходов.",
    "Множество великих людей любили шахматы: Карл Великий, Спиноза, кардинал Ришелье, Пушкин, Стефан Цвейг, Толстой, Тургенев и Тамерлан.",
    "В 2006 году, чемпион мира Владимир Крамник был повергнут компьютером Deep Fritz, что еще раз подчеркнуло мощь шахматных компьютеров. Сегодня шахматные программы часто используются игроками для анализа и улучшения игры.",
    "Первоначально ферзь мог двигаться только на одну клетку по диагонали, затем на две. Так продолжалось до тех пор, пока королева Изабелла Испанская не приказала сделать ферзя (а в Европе его называют королевой) самой сильной фигурой на доске. Из самой слабой фигуры ферзь стал самой сильной",
    "Первое упоминание о шахматах относится в VII в., но свою нынешнюю форму они приобрели лишь спустя восемь веков. Теперь из почти 8 миллиардов человек, живущих на Земле, в шахматы умеют играть около 600 млн.",
    "Прародителем» шахмат считается игра под названием Чатуранга, которая была популярна в Древней Индии. В XIX веке прошла стандартизация игры, после чего стали проводиться международные турниры.",
    "До XIX века черные по правилам тоже могли ходить первыми.",
    "Название «шахматы» происходит от персидских слов «шах» и «мат», которые часто переводятся как «король умер», хотя более точным эквивалентом было бы выражение «король в ловушке» или «королю не убежать",
    "Самая старая из записанных шахматных партий относится к 900 году – это была игра между багдадским летописцем и его учеником.",
    "В средневековых шахматах каждой пешке давали отдельное имя: от купца и врача до ткачихи и трактирщика. Однако, названия не прижились."
    "Самый старый из сохранившихся наборов шахмат был найден на острове Льюис в Северной Шотландии. Он датируется XII веком нашей эры, и предположительно создан в Исландии или Норвегии. Его оригинальное исполение послужило образцом для волшебных шахматных фигур в фильме «Гарри Поттер и философский камень.",
    "Легендарный учёный Алан Тьюринг написал первую в мире компьютерную программу для игры в шахматы в 1951 году. Так как в то время не было машины, способной обработать эту программу, для тестовой игры Тьюрингу пришлось самому выполнять алгоритмические вычисления, делая в несколько минут один ход.",
    "В 1561 году испанский священник Руи Лопес де Сегура написал книгу «Об изобретательности и искусстве игры в шахматы», которая стала первым серьезным изучением этой игры. С именем Руи Лопеса связано создание испанского дебюта, так как наибольшее внимание в своем труде Лопес уделял именно началу игры.",
]

insert_facts_from_list(facts)


@user_private_router.message(Command('fact'))
async def fact_cmd(message: types.Message):
    await message.answer(random.choice(facts))

@user_private_router.message(Command('cluedo'))
async def welcome_to_cluedo(message: types.Message):
    await message.answer("В этом разделе тебя ждёт серия задач на внимательность.\nВ каждой задаче тебе нужно найти определенную улику:\n\n‍🔎 Слабое поле \n🔎 Слабая пешка\n🔎 Ключевая фигура\n🔎 Дебютные следы\n🔎 Замысел соперника\n\nНачнём?")



@user_private_router.message(lambda message: message.text in ["⚡ Тактика", "🎯 Стратегия"])
async def handle_buttons(message):
    if message.text == "⚡ Тактика":
        await message.answer("Выберите тему", reply_markup=tactic_tests)
    elif message.text == "🎯 Стратегия":
        await message.answer("Выберите тему", reply_markup=strategic_tests)

@user_private_router.message(Command('roblox'))
async def welcome2homework(message):
    await message.answer("Поздравляю!\nПодписка на домашние задания оформлена. Задания будут приходить ежедневно в это же время.\nГоржусь тобой!")
    scheduler = AsyncIOScheduler()

    scheduler.add_job(send_homework_for_beginners, 'cron', hour=12, minute=0, kwargs={"message": message})
    scheduler.start()


async def send_homework_for_beginners(bot):
    for user_id in user_level_1_ids:
        try:
            print(f"Начинаем отправку теста для пользователя {user_id}")
            hometest_index, question_index = await get_user_progress(user_id)
            home_test = All_tests[hometest_index]
            user_scores[user_id] = 0

            with open('Welcome2homework.json', 'r', encoding='utf-8') as file:
                data_sticker = json.load(file)

                random_sticker = random.choice(data_sticker)
            # Отправка стикера
            await bot.send_sticker(user_id,
                                   sticker=random_sticker['sticker'])
            print(f"Стикер отправлен для {user_id}")

            await bot.send_message(user_id, random_sticker['text'])
            print(f"Первое сообщение отправлено для {user_id}")

            await asyncio.sleep(3)
            await bot.send_message(user_id,
                                   f"<b>Домашнее задание:</b>\n{home_test['title']} 👀\n"
                                   f"<b>Категория:</b> {home_test['category']}\n"
                                   f"<b>Сложность:</b> {home_test['difficulty']}\n"
                                   f"<b>Количество заданий:</b> {home_test['number_of_ex']}\n\n"
                                   f"<b>Задание:</b> {home_test['text']}\n",
                                   parse_mode=ParseMode.HTML
                                   )
            print(f"Описание теста отправлено для {user_id}")
            await send_next_homework_question_for_beginners(user_id, bot)
        except Exception as e:
            print(f"Ошибка при отправке теста для пользователя {user_id}: {e}")
#    for user_id in user_level_1_ids:
#        hometest_index, question_index = await get_user_progress(user_id)
#        user_scores[user_id] = 0
#        home_test = All_tests[hometest_index]

    #     stickers = await bot.get_custom_emoji_stickers(custom_emoji_ids=["5404683607157514435"])
    #     emoji_placeholder = stickers[0].emoji
    #     utf16_length = len(emoji_placeholder.encode('utf-16-le')) // 2
    #     await bot.send_message(user_id, text=emoji_placeholder, entities=[
    #         MessageEntity(
    #             type=MessageEntityType.CUSTOM_EMOJI,
    #             offset=0,
    #             length=utf16_length,
    #             custom_emoji_id=stickers[0].custom_emoji_id
    #         )
    # ])
#        await bot.send_sticker(user_id, sticker = 'CAACAgIAAxkBAAEOYkZoEO3BKIm6ZQPTRnJXIRotup_aZAACYBIAAhKTCEio8XNd44e_eTYE')
#        await bot.send_message(user_id,
#            f"<b>Домашнее задание:</b> {home_test['title']}\n"
#            f"<b>Категория:</b> {home_test['category']}\n"
#            f"<b>Сложность:</b> {home_test['difficulty']}\n",
#            parse_mode=ParseMode.HTML
#        )
#        print(home_test["id"])
        #await start_fsm_test(message, state, current_test, Prophets)



async def send_next_homework_question_for_beginners(user_id: int, bot: Bot):
    hometest_index, question_index = await get_user_progress(user_id)
    if hometest_index >= len(All_tests):
        return  # Все тесты пройдены

    test = All_tests[hometest_index]
    test_id = All_tests[hometest_index]['id']
    test_name = All_tests[hometest_index]['title']
    user = await bot.get_chat(user_id)
    user_name = user.first_name
    questions = test["questions"]
    if question_index < len(questions):
        question_data = questions[question_index]
        image_file = FSInputFile(question_data["image_path"])
        await bot.send_photo(user_id, photo=image_file)

        poll = await bot.send_poll(
                chat_id=user_id,
                question=question_data["question"],
                options=question_data["options"],
                type="quiz",
                correct_option_id=question_data["correct"],
                is_anonymous=False
            )
        if test_id not in polls:
            polls[test_id] = {}

        polls[test_id][poll.poll.id] = user_id
        print(polls[test_id][poll.poll.id])

    # Проверяем, есть ли доступный вопрос
    if question_index >= len(questions):
        hometest_index += 1
        question_index = 0
        await update_user_progress(user_id, hometest_index, question_index, user_name)
        misquestions.setdefault(user_id, {}).setdefault(test_name, [])
        misquestions_str = " ".join(map(str, misquestions[user_id][test_name]))
        await test_results(user_id, test_name, user_scores)
        insert_user_results(conn, user_name=user_name, test_name=test_name, score=user_scores[user_id], misquestions=misquestions_str)
        return

class BioForm(StatesGroup):
    waiting_for_question = State()

class Wishlist(StatesGroup):
    waiting_for_wishlist_answer = State()

@user_private_router.message(StateFilter(Wishlist.waiting_for_wishlist_answer))
async def wishlist_answers(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    question = "Что бы ты хотел видеть в моей лавке?"
    answer_text = message.text

    save_answer_to_db(user_id,user_name, question, answer_text)
    await message.answer("Спасибо за ответ, передам Жамсо Валерьевичу!")
    await state.clear()  # Очищаем FSM

@user_private_router.message(Command('wish'))
async def what_you_want(message: types.Message, state: FSMContext):
    await message.answer("Долгих дней, приятных ночей, мой юный друг! Поведай мне, что бы ты хотел видеть в моей лавке?")
    await state.set_state(Wishlist.waiting_for_wishlist_answer)

@user_private_router.message(Command('bio'))
async def start_bio(message: types.Message, state: FSMContext):
    """Начинаем анкету с первого вопроса"""
    chat_id = message.chat.id
    await state.update_data(current_question=0)  # Установим индекс на первый вопрос
    await state.set_state(BioForm.waiting_for_question)  # Запускаем FSM

    # Отправляем первый вопрос
    image = FSInputFile(bio_questions[0]['image_path'])
    await bot.send_photo(chat_id, photo=image)
    await message.answer(bio_questions[0]['question'])

@user_private_router.message(BioForm.waiting_for_question)
async def process_bio_answer(message: types.Message, state: FSMContext):
    """Обрабатываем ответ, двигаемся к следующему вопросу"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    answer_text = message.text

    # Получаем текущий индекс вопроса
    data = await state.get_data()
    current_question_index = data.get("current_question", 0)

    # Записываем ответ в SQLite
    save_answer_to_db(user_id, user_name, bio_questions[current_question_index]['question'], answer_text)

    # Переход к следующему вопросу
    next_question_index = current_question_index + 1
    if answer_text[0] == '/': await state.clear()

    if next_question_index < len(bio_questions):  # Если вопросы ещё остались
        await state.update_data(current_question=next_question_index)  # Обновляем индекс
        image = FSInputFile(bio_questions[next_question_index]['image_path'])
        await bot.send_photo(chat_id, photo=image)
        await message.answer(bio_questions[next_question_index]['question'])  # Отправляем вопрос пользователю

    else:
        await message.answer("✅ Анкета завершена! Спасибо за ответы.")
        await state.clear()  # Очищаем FSM

def save_answer_to_db(user_id, user_name, question, answer):
    """Сохраняем ответ в базу данных"""
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('databases/chat_log.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS bio (
        user_id INTEGER,
        student_name TEXT,
        question TEXT, 
        answer TEXT,
        date_time TEXT
    )''')

    cursor.execute('''
        INSERT INTO bio (user_id, student_name, question, answer, date_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, user_name, question, answer, date_time))

    conn.commit()
    conn.close()


class UserStates(StatesGroup):
    waiting_for_question = State()

@user_private_router.message(Command('guru'))
async def handle_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id, text="Задай любой вопрос, мой юный друг... 🕵‍♂️\nЧтобы выйти из режима гуру, введи 'пока'.")
    await state.set_state(UserStates.waiting_for_question)

@user_private_router.message(UserStates.waiting_for_question)
async def process_user_input(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        chat_id = message.chat.id
        question = message.text
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect('databases/chat_log.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO chat_messages (user_id, message, date_time, student_name) 
                VALUES (?, ?, ?, ?)
            ''', (user_id, question, date_time, first_name))
        conn.commit()
        conn.close()
        print(message.from_user.username)
        print(message.from_user.first_name)
        print(question)
        if question.lower() == "пока":
            await bot.send_message(chat_id, text="Увидимся позже 😉")
            await state.clear()
        context = retrieve_info(question)
        print(context)

        #await message.reply("Отправляю запрос на Альфа-Центавра...")
        response = ask_chess_guru(user_id, question)

        if response is None:
            await message.answer("Извините, нейросеть временно недоступна. Попробуйте позже.")
            return

        # Чистим звездочки во ВСЕМ тексте сразу, до проверки на длину
        clean_response = response.replace("*", "")

        MAX_LENGTH = 4096
        if len(clean_response) > MAX_LENGTH:
            # Если текст длинный, аккуратно отправляем его кусками
            for i in range(0, len(clean_response), MAX_LENGTH):
                chunk = clean_response[i:i + MAX_LENGTH]
                # Отправляем без parse_mode, чтобы оборванные теги не вызывали ошибок
                await message.answer(chunk)
        else:
            # Если короткий - отправляем с красивым форматированием
            await bot.send_message(chat_id, clean_response, parse_mode="Markdown")


# async def start_homework(message):
#     for test in All_tests:
#         await message.answer(f"e2-e4!\nДомашнее задание: {test['title']}\nКатегория: {test['category']}\nСложность: {test['difficulty']}\n",parse_mode=ParseMode.HTML)
#         # Итерация по вопросам викторины
#         for question in test["questions"]:
#             photo = FSInputFile(question["image_path"])  # Исправлено
#             await bot.send_photo(chat_id=message.chat.id, photo=photo)
#             # Отправка вопроса как poll
#             await bot.send_poll(
#                 chat_id=message.chat.id,
#                 question=question["question"],  # Текст вопроса
#                 options=question["options"],  # Варианты ответа
#                 type="quiz",  # Тип опроса (викторина)
#                 correct_option_id=question["correct_option_id"],  # Индекс правильного ответа
#                 is_anonymous=False,  # Опрос не анонимный
#             )

@user_private_router.message(Command('quiz'))
async def random_quiz(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    random_test = random.choice(All_tests)
    await message.answer(
        f"<b>Домашнее задание:</b> {random_test['title']}\n"
        f"<b>Категория:</b> {random_test['category']}\n"
        f"<b>Сложность:</b> {random_test['difficulty']}\n",
        parse_mode=ParseMode.HTML
    )
    test_name = random_test['id']
    user_scores[user_id] = 0
    await send_test(user_id, chat_id, test_file=All_tests, test_name=test_name)
class TestStates(StatesGroup):
    waiting_for_question_answer = State()
@user_private_router.message(Command('prophet'))
async def welcome_prophet_test(message: types.Message, state: FSMContext, test_name):
    await message.answer(
        "Это тест на умение видеть будущее. \nТы увидишь позицию, а снизу - пророчество. Прочитай его и найди победу!\n\n Обрати внимание на шахматную нотацию.")
    chat_id = message.chat.id
    notation_image = FSInputFile("brilliants/Notation.png")
    await bot.send_photo(chat_id, photo=notation_image)
    await message.answer("Начнём!")
    await asyncio.sleep(2)
    await start_fsm_test(message, state, test_name, Prophets)
async def start_fsm_test(message: types.Message, state: FSMContext, test_name, file_value):
    user_id = message.from_user.id
    user_states[test_name][user_id] = 0
    user_scores[user_id] = 0

    test_data = None
    for t in file_value:
        if t.get("id") == test_name:
            test_data = t
            break
    if not test_data:
        await message.answer("Тест не найден.")
        return

    await state.update_data(
        test_id=test_data["id"],
        questions=test_data["questions"],
        question_index=0
    )
    await send_next_question(message, state, test_name)

async def send_next_question(message: types.Message, state: FSMContext, test_name):
        """Функция, которая отправляет следующий вопрос пользователю."""
        user_id = message.from_user.id
        chat_id = message.chat.id
        data = await state.get_data()
        questions = data["questions"]
        index = data["question_index"]
        user_name = message.from_user.first_name
        # Проверяем, не вышли ли за предел
        if index >= len(questions):
            misquestions_str = " ".join(map(str, misquestions[user_id][test_name]))
            insert_user_results(conn, user_name, test_name, user_scores[user_id], misquestions_str)
            if "prophet" in test_name.lower():
                await test_results(user_id, test_name, user_scores)
            if "defenders" in test_name.lower():
                await message.answer(f"Количество набранных очков: {user_scores[user_id] }.\nРезультаты будут объявлены в telegram. Спасибо за участие!😉")
            # Сбрасываем состояние
            user_scores[user_id] = 0
            await state.clear()
            return

        current_question = questions[index]
        question_text = current_question.get("question")
        await bot.send_photo(chat_id, photo=FSInputFile(current_question["image_path"]))
        if question_text:
            await bot.send_message(chat_id, question_text)
        # else:
        #     return

        # Переводим пользователя в состояние ожидания ответа
        await state.set_state(TestStates.waiting_for_question_answer)

@user_private_router.message(StateFilter(TestStates.waiting_for_question_answer))
async def check_fsm_answer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    questions = user_data["questions"]
    index = user_data["question_index"]
    test_name = user_data["test_id"]
    current_question = questions[index]
    user_answer = message.text
    if user_answer[0] == '/': await state.clear()

    elif user_answer.lower() == current_question["correct"].lower():
        await message.answer("Правильно, молодец!")
        user_scores[user_id] += 1
    else:
        await message.answer(f"Неверно. Правильный ответ: {current_question['correct']}")
        if user_id not in misquestions:
            misquestions[user_id] = {}
        if test_name not in misquestions[user_id]:
            misquestions[user_id][test_name] = []

        misquestions[user_id][test_name].append(index+1)
    index += 1
    await state.update_data(question_index=index)
    await send_next_question(message, state, test_name)


@user_private_router.message(Command('endgame'))
async def endgame_diagnostics(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_scores[user_id] = 0
    await message.answer(
        "Это тест на знание эндшпиля. Ты всегда играешь за белые фигуры. \nФорма вопроса только одна: побеждают ли белые при идеальной игре с обеих сторон?\nПоехали!")
    await asyncio.sleep(2)
    await send_test(user_id, chat_id, test_file=All_tests, test_name="endgame_diagnostics")
    # await bot.send_message(chat_id, text="Тест завершен")
    # await test_results(user_id, "endgame_diagnostics", user_scores)

@user_private_router.message(Command('challenge'))
async def welcome_to_battle(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    # await bot.send_message(chat_id, text="Добро пожаловать на конкурс решения задач!♟\n\nВсем участникам будет предложен тест.\n\nНайди удобное место, чтобы тебя никто не отвлекал, будет много вопросов.\n\nЖелаю приятного прохождения!😉")
    # await asyncio.sleep(3)
    # await bot.send_message(chat_id, "*** Сегодня тест на знание эндшпиля ***\n\nВо всех задачах ход белых.\n\nФорма вопроса только одна:\n'Побеждают ли белые при идеальной игре с обеих сторон?'\n\n Поехали!")
    # await asyncio.sleep(4)
    # user_scores[user_id] = 0
    # await send_test(user_id, chat_id, test_file=All_tests, test_name="endgame_diagnostics")
    await bot.send_message(chat_id, text="Добро пожаловать на конкурс решения задач!♟\n\nВсем участникам будет предложен тест.\n\nНайди удобное место, чтобы тебя никто не отвлекал, будет много вопросов.\n\nЖелаю приятного прохождения!😉")
    await asyncio.sleep(3)
    await bot.send_message(chat_id, "*** Сегодня тест на искусство защиты ***\n\nВ этих задачах необходимо найти либо спасение фигуры, либо защиту от мата.\nОбрати внимание на шахматную нотацию.")
    notation_image = FSInputFile("brilliants/Notation.png")
    await bot.send_photo(chat_id, photo=notation_image)
    await bot.send_message(chat_id, "Полетели! 🚀")
    await asyncio.sleep(2)
    await start_fsm_test(message, state, "defenders", Defenders)


@user_private_router.message(Command('daily_prophet'))
async def welcome2homework(message):
    await message.answer("Мои поздравления! 🎉 Подписка на ежедневного пророка подписана!\n Тебе будут приходить по два теста на счёт вариантов в день: утром и вечером.\nВ каждом тесте по 12 вопросов.\nРешай их. Поваерь, они принесут тебе большую пользу.")


@user_private_router.message(Command('store'))
async def welcome2store(message):
        # Замените LINK с вашей ссылкой на Mini App
        store_link = "http://watsonstore.tilda.ws/"  # Замените на URL вашего Mini App
        await message.answer(f"Переходи в мою лавку по ссылке: {store_link}")





class TestHomeworkState(StatesGroup):
    waiting_for_homework_answer = State()

async def send_next_homework_question(user_id: int, state: FSMContext, bot: Bot):
    """ Отправляет следующий вопрос пользователю """
    hometest_index, question_index = await get_user_progress(user_id)

    # Проверяем, есть ли доступный тест
    if hometest_index >= len(Prophets):
        return  # Все тесты пройдены

    test = Prophets[hometest_index]
    test_name = Prophets[hometest_index]['title']
    user = await bot.get_chat(user_id)
    user_name = user.first_name
    questions = test["questions"]
    # Проверяем, есть ли доступный вопрос
    if question_index >= len(questions):
        hometest_index += 1
        question_index = 0
        await update_user_progress(user_id, hometest_index, question_index, user_name)
        await state.clear()
        misquestions_str = " ".join(map(str, misquestions[user_id][test_name]))
        await test_results(user_id, test_name, user_scores)
        insert_user_results(conn, user_name=user_name, test_name=test_name, score=user_scores[user_id], misquestions=misquestions_str)
        #await bot.send_message(user_id, "🕺")
        #await bot.send_message(user_id,"Независимо от результата, ты стал лучше 👏\n\nУвидимся завтра в это же время 😉")
        return

    question = questions[question_index]
    image_path = question["image_path"]

    photo = FSInputFile(image_path)
    await bot.send_photo(user_id, photo, caption=f"Вопрос {question_index + 1}: Твой ход?")


#async def welcome2homeworks(message: types.Message):


async def start_new_test_for_all(bot: Bot):
    """Запускает новый тест для всех пользователей ежедневно"""
    for user_id in user_level_3_ids:
        try:
            print(f"Начинаем отправку теста для пользователя {user_id}")
            state = dp.fsm.get_context(user_id=user_id, chat_id=user_id, bot=bot)
            hometest_index, question_index = await get_user_progress(user_id)
            home_test = Prophets[hometest_index]
            user_scores[user_id] = 0

            with open('Welcome2homework.json', 'r', encoding='utf-8') as file:
                data_sticker = json.load(file)

                random_sticker = random.choice(data_sticker)
            # Отправка стикера
            await bot.send_sticker(user_id,
                                   sticker=random_sticker['sticker'])
            print(f"Стикер отправлен для {user_id}")

            await bot.send_message(user_id, random_sticker['text'])
            print(f"Первое сообщение отправлено для {user_id}")

            await asyncio.sleep(3)
            await bot.send_message(user_id,
                                   f"<b>Домашнее задание:</b>\n{home_test['title']} 👀\n"
                                        f"<b>Категория:</b> {home_test['category']}\n"
                                        f"<b>Сложность:</b> {home_test['difficulty']}\n"
                                        f"<b>Количество заданий:</b> {home_test['number_of_ex']}\n\n"
                                        f"<b>Задание:</b> {home_test['text']}\n",
                                        parse_mode=ParseMode.HTML
                                        )
            print(f"Описание теста отправлено для {user_id}")

            await bot.send_message(user_id,
                                   "\nОбрати внимание на шахматную нотацию:")
            notation_image = FSInputFile("brilliants/Notation.png")
            await bot.send_photo(user_id, photo=notation_image)
            print(f"Фото нотации отправлено для {user_id}")

            await send_next_homework_question(user_id, state, bot)
            print(f"Первый вопрос отправлен для {user_id}")

            await state.set_state(TestHomeworkState.waiting_for_homework_answer)
            print(f"Состояние установлено для {user_id}: {await state.get_state()}")

        except Exception as e:
            print(f"Ошибка при отправке теста для пользователя {user_id}: {e}")


@user_private_router.message(StateFilter(TestHomeworkState.waiting_for_homework_answer))
async def handle_user_homework_answer(message: types.Message, state: FSMContext):
    """ Обрабатывает ответ пользователя и отправляет следующий вопрос """
    current_state = await state.get_state()
    print("Текущее состояние:", current_state)  # Проверка состояния
    if current_state != TestHomeworkState.waiting_for_homework_answer.state:
        print("Состояние не соответствует обработчику")
        return

    user_id = message.from_user.id
    if user_id not in user_level_3_ids: #my_ids:
        return  # Обрабатываем только разрешенных пользователей

    hometest_index, question_index = await get_user_progress(user_id)

    if hometest_index >= len(Prophets):
        await message.answer("Вы уже прошли все тесты!")
        return

    test = Prophets[hometest_index]
    questions = test["questions"]
    test_name = test['title']
    user = await bot.get_chat(user_id)
    user_name = user.first_name
    if question_index >= len(questions):
        return  # Нет вопросов

    correct_answer = questions[question_index]["correct"]
    print(correct_answer)

    if message.text.strip().lower() == correct_answer.lower():
        await message.answer("✅ Правильно!")
        user_scores[user_id] +=1

    else:
        await message.answer(f"Неверно. Правильный ответ: {correct_answer}")
        if user_id not in misquestions:
            misquestions[user_id] = {}
        if test_name not in misquestions[user_id]:
            misquestions[user_id][test_name] = []

        misquestions[user_id][test_name].append(question_index+1)

    # Переход к следующему вопросу
    question_index += 1
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update_user_progress(user_id, hometest_index, question_index, user_name, date)
    await send_next_homework_question(user_id, state, message.bot)


### --- ЗАПЛАНИРОВАННЫЕ ОТПРАВКИ ТЕСТОВ --- ###
def schedule_daily_tests(bot: Bot):
    """ Планирует отправку тестов каждый день """
    scheduler.start()
    scheduler.add_job(start_new_test_for_all, "cron", hour="8", minute=0, args=[bot])
    #scheduler.add_job(send_homework_for_beginners, "interval", minutes=2, args=[bot])

@user_private_router.message(Command('state'))
async def check_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"Ваше текущее состояние: {current_state}")
    print(f"Состояние пользователя {message.from_user.id}: {current_state}")

@user_private_router.message(Command('emoji'))
async def extract_custom_emoji_id(message: types.Message):
    if not message.entities:
        await message.reply("❌ В сообщении не найдено сущностей.")
        return

    found_count = 0
    for entity in message.entities:
        if entity.type == MessageEntityType.CUSTOM_EMOJI:
            # Извлекаем часть текста и custom_emoji_id
            emoji_char = message.text[entity.offset:entity.offset + entity.length]
            emoji_id = entity.custom_emoji_id
            found_count += 1

            await message.reply(
                f"✅ Найден премиум-эмодзи:\n"
                f"Emoji: {emoji_char}\n"
                f"custom_emoji_id: {emoji_id}"
            )

    if found_count == 0:
        await message.reply("❗️ В сообщении нет custom_emoji (премиум-эмодзи).")