from aiogram.fsm.state import StatesGroup, State

class LessonStates(StatesGroup):
    format = State()
    datetime = State()
    comment = State()
