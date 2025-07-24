# handlers/user/payments.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ContentType
from database.models import Payment
from database.db import get_db
import os
from config import ADMINS

router = Router()

@router.message(F.content_type == ContentType.DOCUMENT)
async def handle_payment_doc(message: Message):
    if not message.caption or "@YOUR_USERNAME" not in message.caption:
        await message.answer("Пожалуйста, подпишите чек, указав @YOUR_USERNAME в описании.")
        return
    filename = message.document.file_name
    user_id = message.from_user.id

    file_path = f"data/payments/{user_id}_{filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await message.document.download(destination_file=file_path)

    async with get_db() as session:
        payment = Payment(user_id=user_id, filename=os.path.basename(file_path))
        session.add(payment)
        await session.commit()
    await message.answer("✅ Чек получен и сохранён. Спасибо!")
