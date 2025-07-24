# states/homework_states.py
from aiogram.fsm.state import State, StatesGroup

class HomeworkStates(StatesGroup):
    awaiting_homework = State()
