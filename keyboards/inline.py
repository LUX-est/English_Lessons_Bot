# keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_info_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Формат обучения", callback_data="format")],
        [InlineKeyboardButton(text="💬 Часто задаваемые вопросы (FAQ)", callback_data="faq")]
    ])

def get_payment_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить чек", url="https://t.me/max_engliish")]
    ])
