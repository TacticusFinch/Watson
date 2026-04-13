from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

tactic_strategy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚡ Тактика", callback_data="tactic"),
            InlineKeyboardButton(text="🎯 Стратегия", callback_data="strategy"),
        ],
    ],

    input_field_placeholder="Выберите тест 🎯"
)

tactic_tests = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🥷 Бесшумный ниндзя", callback_data="ninja"),
            InlineKeyboardButton(text="🌈 Фантазия", callback_data="fantasy"),
        ],
        [
            InlineKeyboardButton(text="🧬 Изобретательность", callback_data="inventor"),
            InlineKeyboardButton(text="🛡 Неуязвимость", callback_data="defenders"),
        ],
        [
            InlineKeyboardButton(text="🪤 Ловушка или зевок?", callback_data="a"),
            InlineKeyboardButton(text="🪄 Выиграно или нет?", callback_data="winordraw"),
        ],
        [
            InlineKeyboardButton(text="🔮 Пророк", callback_data="prophet_levels"),
        ]
    ],

    input_field_placeholder="Выберите тест 🎯"
)

strategic_tests = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🕵‍ Детективное мышление", callback_data="detective"),
            InlineKeyboardButton(text="🎯 Снайпер", callback_data="sniper"),
            InlineKeyboardButton(text="📚 Теоретические позиции", callback_data="theoretic"),
        ],
        [
            InlineKeyboardButton(text="🌠 Суперзвезда", callback_data="superstar"),
            InlineKeyboardButton(text="🧟‍♂️ Зомби", callback_data="zombie"),
        ]
    ],

    input_field_placeholder="Выберите тест 🎯"
)

next_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Следующая позиция   ➡ ", callback_data="next")]],
    input_field_placeholder="Нажмите далее"
)

next_bio_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Следующий вопрос   ➡ ", callback_data="next_bio")]],
    input_field_placeholder="Нажмите далее"
)

test_might_results = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Узнать результаты ✅ ", callback_data="might_results")]],

)

endgame_diagnostics_results = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Узнать результаты ✅ ", callback_data="endgame_diagnostics_results")]],

)

whiteorblack = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Белые>", callback_data="white"),
            InlineKeyboardButton(text="Черные", callback_data="black")
        ]]
)

easy_prophet_perspectives = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Моими глазами", callback_data="easy_prophet_my_vision"),
            InlineKeyboardButton(text="Глазами соперника", callback_data="easy_prophet_opponent_vision")
        ]
    ]
)

easy_prophet_my_vision = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="easy_prophet1"),
            InlineKeyboardButton(text="2", callback_data="easy_prophet2"),
            InlineKeyboardButton(text="3", callback_data="easy_prophet3"),
            InlineKeyboardButton(text="4", callback_data="easy_prophet4"),
            InlineKeyboardButton(text="5", callback_data="easy_prophet5"),
        ],
        [
            InlineKeyboardButton(text="6", callback_data="easy_prophet6"),
            InlineKeyboardButton(text="7", callback_data="easy_prophet7"),
            InlineKeyboardButton(text="8", callback_data="easy_prophet8"),
            InlineKeyboardButton(text="9", callback_data="easy_prophet9"),
            InlineKeyboardButton(text="10", callback_data="easy_prophet10"),
        ],
        [
            InlineKeyboardButton(text="11", callback_data="easy_prophet11"),
            InlineKeyboardButton(text="12", callback_data="easy_prophet12"),
            InlineKeyboardButton(text="13", callback_data="easy_prophet13"),
            InlineKeyboardButton(text="14", callback_data="easy_prophet14"),
            InlineKeyboardButton(text="15", callback_data="easy_prophet15"),
        ],
        [
            InlineKeyboardButton(text="16", callback_data="easy_prophet16"),
            InlineKeyboardButton(text="17", callback_data="easy_prophet17"),
            InlineKeyboardButton(text="18", callback_data="easy_prophet18"),
            InlineKeyboardButton(text="19", callback_data="easy_prophet19"),
            InlineKeyboardButton(text="20", callback_data="easy_prophet20"),
        ],
        [
            InlineKeyboardButton(text="21", callback_data="easy_prophet21"),
            InlineKeyboardButton(text="22", callback_data="easy_prophet22"),
            InlineKeyboardButton(text="23", callback_data="easy_prophet23"),
            InlineKeyboardButton(text="24", callback_data="easy_prophet24"),
            InlineKeyboardButton(text="25", callback_data="easy_prophet25"),
        ],
    ]
)

easy_prophet_opponent_vision = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="easy_prophet1"),
            InlineKeyboardButton(text="2", callback_data="easy_prophet2"),
            InlineKeyboardButton(text="3", callback_data="easy_prophet3"),
            InlineKeyboardButton(text="4", callback_data="easy_prophet4"),
            InlineKeyboardButton(text="5", callback_data="easy_prophet5"),
        ],
        [
            InlineKeyboardButton(text="6", callback_data="easy_prophet6"),
            InlineKeyboardButton(text="7", callback_data="easy_prophet7"),
            InlineKeyboardButton(text="8", callback_data="easy_prophet8"),
            InlineKeyboardButton(text="9", callback_data="easy_prophet9"),
            InlineKeyboardButton(text="10", callback_data="easy_prophet10"),
        ],
        [
            InlineKeyboardButton(text="11", callback_data="easy_prophet11"),
            InlineKeyboardButton(text="12", callback_data="easy_prophet12"),
            InlineKeyboardButton(text="13", callback_data="easy_prophet13"),
            InlineKeyboardButton(text="14", callback_data="easy_prophet14"),
            InlineKeyboardButton(text="15", callback_data="easy_prophet15"),
        ],
        [
            InlineKeyboardButton(text="16", callback_data="easy_prophet16"),
            InlineKeyboardButton(text="17", callback_data="easy_prophet17"),
            InlineKeyboardButton(text="18", callback_data="easy_prophet18"),
            InlineKeyboardButton(text="19", callback_data="easy_prophet19"),
            InlineKeyboardButton(text="20", callback_data="easy_prophet20"),
        ],
        [
            InlineKeyboardButton(text="21", callback_data="easy_prophet21"),
            InlineKeyboardButton(text="22", callback_data="easy_prophet22"),
            InlineKeyboardButton(text="23", callback_data="easy_prophet23"),
            InlineKeyboardButton(text="24", callback_data="easy_prophet24"),
            InlineKeyboardButton(text="25", callback_data="easy_prophet25"),
        ],
    ]
)



medium_prophet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="3 хода", callback_data="medium_prophet_3"),
            InlineKeyboardButton(text="4 хода", callback_data="medium_prophet_4"),
            InlineKeyboardButton(text="5 ходов", callback_data="medium_prophet_5"),
        ]
    ]


)


medium_prophet_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="medium_prophet_3_1"),
            InlineKeyboardButton(text="2", callback_data="medium_prophet2"),
            InlineKeyboardButton(text="3", callback_data="medium_prophet3"),
            InlineKeyboardButton(text="4", callback_data="medium_prophet4"),
            InlineKeyboardButton(text="5", callback_data="medium_prophet5"),
        ],
        [
            InlineKeyboardButton(text="6", callback_data="prophet6"),
            InlineKeyboardButton(text="7", callback_data="prophet7"),
            InlineKeyboardButton(text="8", callback_data="prophet8"),
            InlineKeyboardButton(text="9", callback_data="prophet9"),
            InlineKeyboardButton(text="10", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="11", callback_data="prophet6"),
            InlineKeyboardButton(text="12", callback_data="prophet7"),
            InlineKeyboardButton(text="13", callback_data="prophet8"),
            InlineKeyboardButton(text="14", callback_data="prophet9"),
            InlineKeyboardButton(text="15", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="16", callback_data="prophet6"),
            InlineKeyboardButton(text="17", callback_data="prophet7"),
            InlineKeyboardButton(text="18", callback_data="prophet8"),
            InlineKeyboardButton(text="19", callback_data="prophet9"),
            InlineKeyboardButton(text="20", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="21", callback_data="prophet6"),
            InlineKeyboardButton(text="22", callback_data="prophet7"),
            InlineKeyboardButton(text="23", callback_data="prophet8"),
            InlineKeyboardButton(text="24", callback_data="prophet9"),
            InlineKeyboardButton(text="25", callback_data="prophet9"),
        ],
    ]
)

medium_prophet_4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="medium_prophet_4_1"),
            InlineKeyboardButton(text="2", callback_data="medium_prophet2"),
            InlineKeyboardButton(text="3", callback_data="medium_prophet3"),
            InlineKeyboardButton(text="4", callback_data="medium_prophet4"),
            InlineKeyboardButton(text="5", callback_data="medium_prophet5"),
        ],
        [
            InlineKeyboardButton(text="6", callback_data="prophet6"),
            InlineKeyboardButton(text="7", callback_data="prophet7"),
            InlineKeyboardButton(text="8", callback_data="prophet8"),
            InlineKeyboardButton(text="9", callback_data="prophet9"),
            InlineKeyboardButton(text="10", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="11", callback_data="prophet6"),
            InlineKeyboardButton(text="12", callback_data="prophet7"),
            InlineKeyboardButton(text="13", callback_data="prophet8"),
            InlineKeyboardButton(text="14", callback_data="prophet9"),
            InlineKeyboardButton(text="15", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="16", callback_data="prophet6"),
            InlineKeyboardButton(text="17", callback_data="prophet7"),
            InlineKeyboardButton(text="18", callback_data="prophet8"),
            InlineKeyboardButton(text="19", callback_data="prophet9"),
            InlineKeyboardButton(text="20", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="21", callback_data="prophet6"),
            InlineKeyboardButton(text="22", callback_data="prophet7"),
            InlineKeyboardButton(text="23", callback_data="prophet8"),
            InlineKeyboardButton(text="24", callback_data="prophet9"),
            InlineKeyboardButton(text="25", callback_data="prophet9"),
        ],
    ]
)

medium_prophet_5 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="medium_prophet_5_1"),
            InlineKeyboardButton(text="2", callback_data="medium_prophet2"),
            InlineKeyboardButton(text="3", callback_data="medium_prophet3"),
            InlineKeyboardButton(text="4", callback_data="medium_prophet4"),
            InlineKeyboardButton(text="5", callback_data="medium_prophet5"),
        ],
        [
            InlineKeyboardButton(text="6", callback_data="prophet6"),
            InlineKeyboardButton(text="7", callback_data="prophet7"),
            InlineKeyboardButton(text="8", callback_data="prophet8"),
            InlineKeyboardButton(text="9", callback_data="prophet9"),
            InlineKeyboardButton(text="10", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="11", callback_data="prophet6"),
            InlineKeyboardButton(text="12", callback_data="prophet7"),
            InlineKeyboardButton(text="13", callback_data="prophet8"),
            InlineKeyboardButton(text="14", callback_data="prophet9"),
            InlineKeyboardButton(text="15", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="16", callback_data="prophet6"),
            InlineKeyboardButton(text="17", callback_data="prophet7"),
            InlineKeyboardButton(text="18", callback_data="prophet8"),
            InlineKeyboardButton(text="19", callback_data="prophet9"),
            InlineKeyboardButton(text="20", callback_data="prophet9"),
        ],
        [
            InlineKeyboardButton(text="21", callback_data="prophet6"),
            InlineKeyboardButton(text="22", callback_data="prophet7"),
            InlineKeyboardButton(text="23", callback_data="prophet8"),
            InlineKeyboardButton(text="24", callback_data="prophet9"),
            InlineKeyboardButton(text="25", callback_data="prophet9"),
        ],
    ]
)

hard_prophet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="8 ходов", callback_data="hard_prophet8"),
            InlineKeyboardButton(text="10 ходов", callback_data="hard_prophet10"),
            InlineKeyboardButton(text="12 ходов", callback_data="hard_prophet12")
    ]
    ]
)



prophet_levels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            # Два хода в уме + Глазами соперника
            InlineKeyboardButton(text="Легкий 🐥", callback_data="easy_prophet"),

            # 3, 4, 5 ходов в уме
            InlineKeyboardButton(text="Средний 🦊", callback_data="medium_prophet"),

            # 8 10 12 14 16 18 20 22 24 26 28 30 ходов в уме
            InlineKeyboardButton(text="Сложный 🦁", callback_data="hard_prophet"),
        ]
    ]
)


winordraw_tests = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="winordraw1"),
            InlineKeyboardButton(text="2", callback_data="winordraw2"),
            InlineKeyboardButton(text="3", callback_data="winordraw3")
    ]
    ]
)


defend = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Защита от мата", callback_data="mate_defend"),
            InlineKeyboardButton(text="Спаси фигуру", callback_data="piece_defend")

        ]
    ]
)

store = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Открыть магазин", callback_data="openstore")
        ]
    ]
)
