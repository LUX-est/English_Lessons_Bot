from aiogram.fsm.state import State, StatesGroup

class QuestionStates(StatesGroup):
    waiting_for_question_text = State()
