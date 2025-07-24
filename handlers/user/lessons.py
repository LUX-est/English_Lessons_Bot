from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import get_db
from database.models import LessonSlot
from sqlalchemy import select

router = Router()

@router.message(F.text == "📆 Записаться на урок")
async def show_slots(message: Message):
    async with get_db() as session:
        result = await session.execute(select(LessonSlot).where(LessonSlot.booked_by == None))
        slots = result.scalars().all()

    if not slots:
        await message.answer("Извините, сейчас нет доступных слотов для записи.")
        return

    buttons = [
        [InlineKeyboardButton(text=slot.datetime_str, callback_data=f"book_{slot.id}")]
        for slot in slots
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Выберите удобное время для урока:", reply_markup=kb)

@router.callback_query()
async def process_booking(callback: CallbackQuery):
    if not callback.data or not callback.data.startswith("book_"):
        return  

    slot_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    async with get_db() as session:
        result = await session.execute(select(LessonSlot).where(LessonSlot.id == slot_id))
        slot = result.scalars().first()
        if not slot:
            await callback.answer("Этот слот больше недоступен.", show_alert=True)
            return
        if slot.booked_by is not None:
            await callback.answer("Этот слот уже занят.", show_alert=True)
            return

        slot.booked_by = user_id
        await session.commit()

    await callback.answer("Вы успешно записались на урок!", show_alert=True)
    await callback.message.edit_text(f"Вы записаны на урок: {slot.datetime_str}")
