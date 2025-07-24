# handlers/user/homework.py
from aiogram import Router, F
from aiogram.types import Message
from database.models import Homework
from database.db import get_db
from sqlalchemy import select

router = Router()

@router.message(F.text == "🧠 Дополнительное ДЗ")
async def get_homework(message: Message):
    async with get_db() as session:
        result = await session.execute(
            select(Homework).order_by(Homework.created_at.desc())
        )
        last_homework = result.scalars().first()
        if last_homework:
            await message.answer(f"📝 Актуальное ДЗ:\n\n{last_homework.content}")
        else:
            await message.answer("🔍 Пока нет дополнительного ДЗ.")
