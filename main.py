# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db

from handlers.user import registration, menu, lessons, questions, homework, info, payments
from handlers.admin import panel, manage_lessons, homework_admin, view_questions, students

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(registration.router)
    dp.include_router(menu.router)
    dp.include_router(lessons.router)
    dp.include_router(questions.router)
    dp.include_router(homework.router)
    dp.include_router(info.router)
    dp.include_router(payments.router)

    dp.include_router(panel.router)
    dp.include_router(manage_lessons.router)
    dp.include_router(homework_admin.router)
    dp.include_router(view_questions.router)
    dp.include_router(students.router)

    await init_db()

    logging.info("Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
