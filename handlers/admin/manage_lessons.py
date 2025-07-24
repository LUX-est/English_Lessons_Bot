# handlers/admin/manage_lessons.py
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from database.models import LessonSlot
from database.db import get_db
from sqlalchemy import select, delete
from config import ADMINS
from states.lesson_states import LessonBookingStates

router = Router()

@router.message(F.text == "🗓 Поставить урок")
async def request_lesson_time(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    await message.answer("📅 Введите слот в формате: дд.мм.гггг чч:мм")
    await state.set_state(LessonBookingStates.waiting_for_slot_choice)

@router.message(StateFilter(LessonBookingStates.waiting_for_slot_choice))
async def add_lesson(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    datetime_str = message.text.strip()
    async with get_db() as session:
        result = await session.execute(select(LessonSlot).where(LessonSlot.datetime_str == datetime_str))
        exists = result.scalars().first()
        if exists:
            await message.answer("❗ Такой слот уже существует.")
            return
        slot = LessonSlot(datetime_str=datetime_str)
        session.add(slot)
        await session.commit()
        await message.answer("✅ Слот успешно добавлен.")
    await state.clear()
