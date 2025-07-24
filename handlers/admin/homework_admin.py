# handlers/admin/homework_admin.py
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from database.models import Homework
from database.db import get_db
from config import ADMINS
from states.homework_states import HomeworkStates

router = Router()

@router.message(F.text == "📌 Добавить доп. ДЗ")
async def ask_homework(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    await message.answer("🧠 Введите текст дополнительного ДЗ:")
    await state.set_state(HomeworkStates.awaiting_homework)

@router.message(StateFilter(HomeworkStates.awaiting_homework))
async def save_homework(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    async with get_db() as session:
        hw = Homework(content=message.text)
        session.add(hw)
        await session.commit()
        await message.answer("✅ Дополнительное ДЗ добавлено.")
    await state.clear()
