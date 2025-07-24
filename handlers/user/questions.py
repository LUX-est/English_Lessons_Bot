from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.models import Question
from database.db import get_db
from states.question_states import QuestionStates

router = Router()

@router.message(F.text == "❓Вопрос преподавателю")
async def ask_question(message: Message, state: FSMContext):
    await message.answer("✍ Напишите свой вопрос:")
    await state.set_state(QuestionStates.waiting_for_question_text)

@router.message(StateFilter(QuestionStates.waiting_for_question_text))
async def save_question(message: Message, state: FSMContext):
    
    if message.text.startswith('/'):
        await state.clear()
        return
    async with get_db() as session:
        question = Question(user_id=message.from_user.id, text=message.text)
        session.add(question)
        await session.commit()
    await message.answer("✅ Вопрос отправлен!")
    await state.clear()
