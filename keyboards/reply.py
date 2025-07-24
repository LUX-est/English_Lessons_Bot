# keyboards/reply.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📆 Записаться на урок")],
            [KeyboardButton(text="❓Вопрос преподавателю")],
            [KeyboardButton(text="🧠 Дополнительное ДЗ")],
            [KeyboardButton(text="ℹ Общая информация")],
            [KeyboardButton(text="💳 Оплата")]
        ],
        resize_keyboard=True
    )

def get_admin_panel():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Поставить урок")],
            [KeyboardButton(text="📌 Добавить доп. ДЗ")],
            [KeyboardButton(text="❓Посмотреть вопросы")],
            [KeyboardButton(text="👥 Ученики")]
        ],
        resize_keyboard=True
    )
