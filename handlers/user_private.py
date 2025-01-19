import asyncio
import os
import random
import re

from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, PollAnswer
from aiogram.filters.state import StateFilter
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_instance import bot
from databases.facts_db import insert_facts_from_list


from keyboards.inline import tactic_tests, strategic_tests, next_button, test_might_results
from keyboards.reply import tactic_strategy_button

MEMES_FOLDER = "memes"
PUZZLE_FOLDER = "puzzles"
BRILLIANTS_FOLDER = "brilliants"
CHAT_ID = None

user_private_router = Router()




All_tests = [
    {
        "id": 1,
        "title": "Бесшумный ниндзя",
        "category": "Тактика",
        "difficulty": "Легкий",
        "number": "1",
        "questions": [
            {
                "question": "Вопрос 1. За какое наименьшее количество ходов белый конь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/1.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 2. За какое наименьшее количество ходов белая ладья сможет сделать шах королю, оставаясь незамеченной?",
                "image_path": "ninja/2.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 2
            },
            {
                "question": "Вопрос 3. За какое наименьшее количество ходов белый ферзь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/3.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 1
            },
            {
                "question": "Вопрос 4. За какое наименьшее количество ходов белый слон сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/4.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 5. За какое наименьшее количество ходов белый слон сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/5.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 6. За какое наименьшее количество ходов белый ферзь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/6.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 1
            },
            {
                "question": "Вопрос 7. За какое наименьшее количество ходов белый ферзь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/7.png",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 8. За какое наименьшее количество ходов черный конь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/8.png",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 9. За какое наименьшее количество ходов черная ладья сможет сделать шах королю, оставаясь незамеченной?",
                "image_path": "ninja/9.png",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 0
            },
            {
                "question": "Вопрос 10. За какое наименьшее количество ходов черная ладья сможет сделать шах королю, оставаясь незамеченной?",
                "image_path": "ninja/10.png",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 2
            },
            {
                "question": "Вопрос 11. За какое наименьшее количество ходов белый ферзь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/11.png",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 2
            },
            {
                "question": "Вопрос 12. За какое наименьшее количество ходов черный конь сможет сделать шах королю, оставаясь незамеченным?",
                "image_path": "ninja/12.png",
                "options": ["Это невозможно", "4", "5", "6"],
                "correct_option_id": 3
            },
        ],
    },

    {
        "id": 2,
        "title": "Счетчик шахов",
        "category": "Тактика",
        "dificulty": "Легкий",
        "number": "2",
        "questions": [
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["1", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 2
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 1
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции??",
                "image_path": "",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 1
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "2", "3", "4"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 3
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 0
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 2
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "3", "4", "5"],
                "correct_option_id": 2
            },
            {
                "question": "Вопрос 1. Ход белых. Сколько всевозможных шахов можно поставить в этой позиции?",
                "image_path": "",
                "options": ["Это невозможно", "4", "5", "6"],
                "correct_option_id": 3
            },
        ],
    }


]

user_states = {
    'might': {},
    'style': {},
    'ninja': {}
}

polls = {
    'might': {},
    'style': {},
    'ninja': {}
}

user_scores = {}
@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Давай посмотрим, что я могу тебе предложить 😉\n\n'
                         "🔹 Пройти тест силы.\n"
                         "🔹 Определить твой стиль игры. (в разработке)\n"
                         "🔹 Нестандартные тренажеры (в разработке)\n"
                         "🔹 Рассмешить тебя (мем)\n"
                         "🔹 Рассказать мудрость\n"
                         "🔹 Рассказать интересный факт\n\n"
                          "🛠 Для начала работы нажмите кнопку ниже или используйте меню\n\n"
                         "/start - перезапустить бота\n"
                         "/test - тест силы\n"
                         "/style - найти свой стиль\n"
                         "/cluedo - детективное мышление (в разработке)\n"
                         "/train - тактические тренажеры\n"
                         "/mem4gem - мемас за алмаз\n"
                         "/meme - шахматный мем\n"
                         "/pearl - мудрость\n"
                         "/fact - интересный факт\n"
                         "/danet - правда или ложь (в разработке)\n"
                         "/roblox - сыграть в роблокс"
                         )


might_questions = [
    {
        "question": "Вопрос 1. Выгодно ли белым съесть слона?",
        "image_path": "tests/1.png",
        "options": ["Да", "Нет"],
        "correct": 1,
    },
    {
        "question": "Вопрос 2. Могут ли белые съесть коня на f6?",
        "image_path": "tests/2.png",
        "options": ["Да", "Нет"],
        "correct": 1,
    },
    {
        "question": "Вопрос 3. Могут ли белые съесть слона на h3?",
        "image_path": "tests/3.png",
        "options": ["Да", "Нет"],
        "correct": 1,
    },
    {
        "question": "Вопрос 4. Могут ли черные съесть пешку d4",
        "image_path": "tests/4.png",
        "options": ["Да", "Нет"],
        "correct": 0,
    },
    {
        "question": "Вопрос 5. Сколько в этой позиции всевозможных шахов?",
        "image_path": "tests/5.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 6. Сколько в этой позиции всевозможных съедений?",
        "image_path": "tests/6.png",
        "options": ["3", "4", "5", "6"],
        "correct": 2,
    },
    {
        "question": "Вопрос 7. Могут ли белые поставить мат?",
        "image_path": "tests/7.png",
        "options": ["Да", "Нет"],
        "correct": 0,
    },
    {
        "question": "Вопрос 8. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "tests/8.png",
        "options": ["Это невозможно", "2", "3", "4"],
        "correct": 3,
    },
    {
        "question": "Вопрос 9. Чья позиция лучше?",
        "image_path": "tests/9.png",
        "options": ["Белых", "Черных", "Позиция равна"],
        "correct": 0,
    },
    {
        "question": "Вопрос 10. За какое минимальное количество ходов черные смогут поставить мат?",
        "image_path": "tests/10.png",
        "options": ["1", "2", "3", "4"],
        "correct": 1,
    },
    {
        "question": "Вопрос 11. Выгодно ли белым брать слона d8?",
        "image_path": "tests/11.png",
        "options": ["Да", "Нет"],
        "correct": 0,
    },
    {
        "question": "Вопрос 12. Чем закончится игра при идеальной игре с обеих сторон?",
        "image_path": "tests/12.png",
        "options": ["Ничья", "Белые победят"],
        "correct": 0,
    },
    {
        "question": "Вопрос 13. Какая защита от мата самая лучшая?",
        "image_path": "tests/13.png",
        "options": ["g6", "Ne6", "Ne8", "Nh5"],
        "correct": 3,
    },
    {
        "question": "Вопрос 14. Ход белых. Успеет ли черный король задержать пешку?",
        "image_path": "tests/14.png",
        "options": ["Да", "Нет"],
        "correct": 0,
    },
    {
        "question": "Вопрос 15. Оцените ход Rd6",
        "image_path": "tests/15.png",
        "options": ["Сильный, это сочетание отвлечения и уничтожения защиты", "Это ошибка"],
        "correct": 1,
    },
    {
        "question": "Вопрос 16. Во сколько ходов черные ставят мат?",
        "image_path": "tests/16.png",
        "options": ["Здесь нет мата", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 17. Ход черных. Как бы вы сыграли?",
        "image_path": "tests/17.png",
        "options": ["g6", "Qb6", "f6"],
        "correct": 1,
    },
    {
        "question": "Вопрос 18. Ход черных. Как бы вы сыграли?",
        "image_path": "tests/18.png",
        "options": ["Rb6", "Re2", "Ke8", "Rb5"],
        "correct": 0,
    },
    {
        "question": "Вопрос 19. Черные планируют сыграть Bb5. Оцените это решение.",
        "image_path": "tests/19.png",
        "options": ["Ход хороший, препятствует маневру Bc4->Bd5 и вскроет линию для ладьи", "Это плохой размен, ведет к выгоде белых", "Ход нейтральный, позицию не портит"],
        "correct": 1,
    },
    {
        "question": "Вопрос 20. Как бы вы сыграли?",
        "image_path": "tests/20.png",
        "options": ["Ke4", "e3", "e4", "Kd2"],
        "correct": 0,
    },
    {
        "question": "Вопрос 21. Как черным укрепить пешку d5?",
        "image_path": "tests/21.png",
        "options": ["Nf6", "Be6", "e6"],
        "correct": 2,
    },
    {
        "question": "Вопрос 22. Работает ли комбинация Сh7->Kg5?",
        "image_path": "tests/22.png",
        "options": ["Да", "Нет"],
        "correct": 1,
    },
    {
        "question": "Вопрос 23. Ход белых. Чем закончится партия?",
        "image_path": "tests/23.png",
        "options": ["Победа белых", "Ничья"],
        "correct": 0,
    },
    {
        "question": "Вопрос 24. Ход белых. Оцените ход Bh6",
        "image_path": "tests/24.png",
        "options": ["Сильный, разменивается сильный слон на g7", "Ход нейтральный, позицию не портит", "Это зевок"],
        "correct": 2,
    },
    {
        "question": "Вопрос 25. Стоит ли черным взять коня на c3?",
        "image_path": "tests/25.png",
        "options": ["Да, размен ведет к выгоде черным", "Слон сейчас сильнее коня, лучше не меняться", "Ход не меняет оценку позиции"],
        "correct": 0,
    },

]

ninja_questions = [
    {
        "question": "Вопрос 1. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/1.png",
        "options": ["4", "5", "6", "Это невозможно"],
        "correct": 2,
    },
    {
        "question": "Вопрос 2. За сколько ходов подряд белый конь сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/2.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 3. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/3.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 4. За сколько ходов подряд белый конь сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/4.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 5. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/5.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 6. За сколько ходов подряд белый конь сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/6.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 7. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/7.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 8. За сколько ходов подряд белый конь сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/8.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 9. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/9.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 10. За сколько ходов подряд белый конь сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/10.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 11. За сколько ходов подряд белый слон сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/11.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 12. За сколько ходов подряд белый конь сможет сделать шах королю, оставаясь незамеченным?",
        "image_path": "ninja/12.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
]

checks_questions = [
    {
        "question": "Вопрос 1. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/1.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 2. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/2.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 3. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/3.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 4. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/4.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 5. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/5.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 6. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/6.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 7.Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/7.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 8. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/8.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 9. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/9.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 10. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/10.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
    {
        "question": "Вопрос 11. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/11.png",
        "options": ["2", "3", "4", "Это невозможно"],
        "correct": 1,
    },
    {
        "question": "Вопрос 12. Сколько всевозможных шахов есть в этой позиции?",
        "image_path": "homeworks/checks/12.png",
        "options": ["2", "3", "4", "5"],
        "correct": 2,
    },
]
style_questions = [
    {
        "question": "Что бы вы выбрали: Бриллиантовый ход или партию с точностью 99% ?",
        "image_path": "style/1.png",
        "options": ["Бриллиантовый ход", "Аккуратная партия"],
    },
    {
        "question": "Какой бы ход в этой позиции вы предпочли?",
        "image_path": "style/2.png",
        "options": ["вариант 1", "вариант 2"],
    },
    {
        "question": "У тебя есть интересная жертва коня на f7, как бы ты оценил этот ход?",
        "image_path": "style/3.png",
        "options": ["Очень сильный. После Фh5 - Kpe6, чувствую, что выиграю", "Сомнительно, нужно просчитать и проверить все возможные варианты"],
    },
    {
        "question": "Какую бы суперсилу вы выбрали?",
        "image_path": "style/4.png",
        "options": ["Абсолютное знание всех дебютов", "Самая быстрая скорость в интернете"],
    }

]

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
    chat_id = message.from_user.id
    user_states['might'][user_id] = 0
    user_scores[user_id] = 0
    await send_might_question(chat_id, user_id)

async def send_might_question(chat_id, user_id):
    current_question_index = user_states['might'][user_id]
    question_data = might_questions[current_question_index]
    image_file = FSInputFile(question_data["image_path"])
    # with open(question_data["image_path"], "rb") as image_file:
    await bot.send_photo(chat_id, photo=image_file)
    poll = await bot.send_poll(
        chat_id=chat_id,
        question=question_data["question"],
        options=question_data["options"],
        type="quiz",
        correct_option_id=question_data["correct"],
        is_anonymous=False
    )

    polls['might'][poll.poll.id] = user_id


@user_private_router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    poll_id = poll_answer.poll_id
    user_id = polls['might'].get(poll_id)
    # Проверяем, есть ли пользователь в состоянии
    if user_id:
        current_question_index = user_states['might'].get(user_id,0)
        #   print(user_states)
        #Переходим к следующему вопросу
        next_question_index = current_question_index + 1
        if next_question_index < len(might_questions):
            # Если есть следующий вопрос, обновляем индекс
            user_states['might'][user_id] = next_question_index
            #print(user_states['might'])
            #print("Поле ответа ")
            #print(might_questions[current_question_index]['correct'])
            user_response = poll_answer.option_ids
            #print(poll_answer.option_ids)
            #print("Ответ пользователя" )
            #print(user_response[0])
            if user_response[0] == might_questions[current_question_index]['correct']:
                user_scores[user_id] += 1
                print("Очки ")
                print(user_scores[user_id])
            await send_might_question(chat_id=poll_answer.user.id, user_id=user_id)

        else:
            user_response = poll_answer.option_ids
            if user_response[0] == might_questions[current_question_index]['correct']:
                user_scores[user_id] += 1
                print("Финальное количество очков: ")
                print(user_scores[user_id])
            user_states['might'].pop(user_id)
            polls['might'].pop(poll_id, None)
            # Если вопросов больше нет, заканчиваем опрос
            await bot.send_message(
            chat_id=user_id,
            text="🎉 Тест завершен!",
            reply_markup = test_might_results
        )

    else:
        user_id = polls['style'].get(poll_id)
        if user_id:
            current_question_index = user_states['style'].get(user_id, 0)
            # Переходим к следующему вопросу
            next_question_index = current_question_index + 1
            print(next_question_index)
            if next_question_index < len(style_questions):
                # Если есть следующий вопрос, обновляем индекс
                user_states['style'][user_id] = next_question_index
                await send_style_questions(chat_id=poll_answer.user.id, user_id=user_id)
            else:
                user_states['style'].pop(user_id)
                polls['style'].pop(poll_id, None)
                # Если вопросов больше нет, заканчиваем опрос
                await bot.send_message(
                    chat_id=user_id,
                    text="🎉 Данные получены! Спасибо за участие.",
                ),
        else: # Здесь добавляем обработку теста Ninja
            user_id = polls['ninja'].get(poll_id)

            if user_id:
                current_question_index = user_states['ninja'].get(user_id, 0)
                next_question_index = current_question_index + 1

            if next_question_index < len(ninja_questions):
                user_states['ninja'][user_id] = next_question_index
                user_response = poll_answer.option_ids

            if user_response[0] == ninja_questions[current_question_index]['correct']:
                user_scores[user_id] += 1
                print(f"Очки для Ninja: {user_scores[user_id]}")
                await send_ninja_questions(chat_id=poll_answer.user.id, user_id=user_id)
        
            else:
                user_response = poll_answer.option_ids
                if user_response[0] == ninja_questions[current_question_index]['correct']:
                    user_scores[user_id] += 1
                print(f"Финальное количество очков для Ninja: {user_scores[user_id]}")

        user_states['ninja'].pop(user_id)
        polls['ninja'].pop(poll_id, None)

        await bot.send_message(
            chat_id=user_id,
            text="🎉 Ninja тест завершен! Спасибо за участие.",)

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

@user_private_router.message(Command('style'))
async def send_welcome_style(message: types.Message):
    await message.answer("Это тест на определение твоего стиля игры. Кто ты: ассасин, волшебник или вяленая рыба?")
    await asyncio.sleep(2)
    await start_style_test(message)


async def start_style_test(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states['style'][user_id] = 0
    await send_style_questions(chat_id, user_id)


async def send_style_questions(chat_id, user_id):
    current_question_index = user_states['style'][user_id]
    question_data = style_questions[current_question_index]
    image_file = FSInputFile(question_data["image_path"])
    await bot.send_photo(chat_id, photo=image_file)
    poll = await bot.send_poll(
            chat_id=chat_id,
            question=question_data["question"],
            options=question_data["options"],
            type="regular",
            is_anonymous=False
    )
    polls['style'][poll.poll.id] = user_id

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
    await send_ninja_questions(chat_id, user_id)
# async def define_style(message: types.Message)
async def send_ninja_questions(chat_id, user_id):
    current_question_index = user_states['ninja'][user_id]
    question_data = ninja_questions[current_question_index]
    print(question_data)
    image_file = FSInputFile(question_data["image_path"])
    await bot.send_photo(chat_id, photo=image_file)

    poll = await bot.send_poll(
        chat_id=chat_id,
        question=question_data["question"],
        options=question_data["options"],
        type="quiz",
        correct_option_id=question_data["correct"],
        is_anonymous=False
    )
    print(user_states['ninja'])
    polls['ninja'][poll.poll.id] = user_id


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
    await message.answer("Поздравляю!\nПодписка на домашние задания оформлена. Задания будут приходить ежедневно в 12 часов дня.\nГоржусь тобой!")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(homework, 'interval', minutes=1440, kwargs={"message": message})
    scheduler.start()

async def homework(message):
    await start_homework(message)

async def start_homework(message):
    for test in All_tests:
        await message.answer(f"e2-e4!\nДомашнее задание: {test['title']}\nКатегория: {test['category']}\nСложность: {test['difficulty']}\n",parse_mode=ParseMode.HTML)
        # Итерация по вопросам викторины
        for question in test["questions"]:
            photo = FSInputFile(question["image_path"])  # Исправлено
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            # Отправка вопроса как poll
            await bot.send_poll(
                chat_id=message.chat.id,
                question=question["question"],  # Текст вопроса
                options=question["options"],  # Варианты ответа
                type="quiz",  # Тип опроса (викторина)
                correct_option_id=question["correct_option_id"],  # Индекс правильного ответа
                is_anonymous=False,  # Опрос не анонимный
            )