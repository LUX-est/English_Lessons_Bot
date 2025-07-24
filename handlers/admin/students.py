# handlers/admin/students.py
from aiogram import Router, F
from aiogram.types import Message
from database.models import User, LessonSlot
from database.db import get_db
from config import ADMINS
from sqlalchemy import select

router = Router()

@router.message(F.text == "👥 Ученики")
async def list_users(message: Message):
    if message.from_user.id not in ADMINS:
        return
    async with get_db() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        if not users:
            await message.answer("Пользователей нет.")
            return
        for u in users:
            await message.answer(
                f"<b>{u.name}</b>, {u.age} лет\n"
                f"Уровень: {u.level}\n"
                f"Цель: {u.goal_time}\n"
                f"Формат: {u.format}\n"
                f"Занятий в неделю: {u.weekly_lessons}\n"
                f"Темы: {u.topics}\n"
                f"VPN: {u.vpn}\n"
                f"Пожелания: {u.wishes}",
                parse_mode="HTML"
            )

@router.message(F.text == "📂 Чеки")
async def list_payments(message: Message):
    if message.from_user.id not in ADMINS:
        return
    from database.models import Payment
    async with get_db() as session:
        result = await session.execute(select(Payment).order_by(Payment.created_at.desc()).limit(20))
        payments = result.scalars().all()
        if not payments:
            await message.answer("Чеков не найдено.")
            return
        for p in payments:
            user_result = await session.execute(select(User).where(User.tg_id == p.user_id))
            user = user_result.scalars().first()
            user_name = user.name if user else "Пользователь"
            await message.answer(f"📄 Чек от {user_name} ({p.user_id}): файл <code>{p.filename}</code>", parse_mode="HTML")
