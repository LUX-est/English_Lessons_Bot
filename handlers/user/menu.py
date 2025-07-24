# handlers/user/menu.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import get_main_menu
from keyboards.inline import get_info_menu, get_payment_button

router = Router()

@router.message(F.text == "ℹ Общая информация")
async def info(message: Message):
    await message.answer("📘 Выберите, что вас интересует:", reply_markup=get_info_menu())

@router.message(F.text == "💳 Оплата")
async def payment(message: Message):
    await message.answer("💸 Оплатите на карту 1234 5678 9012 3456 и отправьте чек преподавателю.", reply_markup=get_payment_button())
