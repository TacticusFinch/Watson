from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

tests_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🥷 Бесшумный ниндзя",url='https://lichess.org/study/cHFVOBxj'),
            InlineKeyboardButton(text="🌀 Фантазия", callback_data="fantasy_test"),
        ],
        [
            InlineKeyboardButton(text="🔍 Визуализация", callback_data="visualisation_test"),
            InlineKeyboardButton(text="🛡️ Неуязвимость", callback_data="invulnerability_test"),
        ],
        [
            InlineKeyboardButton(text="➡️ Следующий", callback_data="next_task"),
            InlineKeyboardButton(text="📖 Помощь", url="https://example.com/help")
        ],
    ],

    input_field_placeholder="Выберите тест 🎯"
)

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
            InlineKeyboardButton(text="🛡 Неуязвимость", callback_data="inventor"),
        ],
        [
            InlineKeyboardButton(text="🪤 Ловушка или зевок?", callback_data="a"),
            InlineKeyboardButton(text="🪄 Высшая магия", callback_data="b"),
        ],
    ],

    input_field_placeholder="Выберите тест 🎯"
)

strategic_tests = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🕵‍ Детективное мышление", callback_data="detective"),
            InlineKeyboardButton(text="🎯 Снайпер", callback_data="sniper"),
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

test_might_results = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Узнать результаты ✅ ", callback_data="might_results")]],

)


