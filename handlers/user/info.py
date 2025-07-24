# handlers/user/info.py
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from keyboards.inline import get_info_menu

router = Router()

@router.callback_query(lambda c: c.data == "format")
async def show_format(call: CallbackQuery):
    text = (
        "📚 Формат обучения:\n\n"
        "1. Упор на разговорную практику\n"
        "2. Теория и ресурсы — Google Classroom и Notion\n"
        "3. Без лишней теории — только практичное\n"
        "4. Учебники по желанию\n"
        "5. Цель — быстрые и ощутимые результаты"
    )
    await call.message.edit_text(text, reply_markup=get_info_menu())

@router.callback_query(lambda c: c.data == "faq")
async def show_faq(call: CallbackQuery):
    text = (
        "❓ Часто задаваемые вопросы:\n\n"
        "• Сколько раз в неделю заниматься?\n"
        "• Сколько уделять времени в неделю?\n"
        "• Где брать материалы?\n"
        "• Как ускорить прогресс?\n"
        "• Что делать, если не получится прийти?"
    )
    await call.message.edit_text(text, reply_markup=get_info_menu())
