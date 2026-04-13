from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

tactic_strategy_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚡ Тактика"),
            KeyboardButton(text="🎯 Стратегия"),
        ],
    ],
    resize_keyboard=True,

    input_field_placeholder="Выберите вариант"
)

del_keyboard = ReplyKeyboardRemove()

