from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from config import ADMINS
from keyboards.reply import get_admin_panel

router = Router()

@router.message(Command(commands=["admin"]))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("⛔ Доступ запрещён.")
        return
    await message.answer("🛠 Панель администратора", reply_markup=get_admin_panel())
