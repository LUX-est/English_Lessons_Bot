# handlers/admin/view_questions.py
from aiogram import Router, F
from aiogram.types import Message
from database.models import Question, User
from database.db import get_db
from config import ADMINS
from sqlalchemy import select

router = Router()

@router.message(F.text == "❓Посмотреть вопросы")
async def view_questions(message: Message):
    if message.from_user.id not in ADMINS:
        return
    async with get_db() as session:
        result = await session.execute(select(Question).order_by(Question.created_at.desc()).limit(20))
        questions = result.scalars().all()
        if not questions:
            await message.answer("❌ Вопросов нет.")
            return
        for q in questions:
            user_result = await session.execute(select(User).where(User.tg_id == q.user_id))
            user = user_result.scalars().first()
            user_name = user.name if user else "Пользователь"
            await message.answer(f"🧑‍🎓 {user_name} ({q.user_id}):\n{q.text}")
