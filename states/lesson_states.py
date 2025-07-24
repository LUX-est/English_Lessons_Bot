# states/lesson_states.py
from aiogram.fsm.state import State, StatesGroup

class LessonBookingStates(StatesGroup):
    waiting_for_slot_choice = State()
    confirming_booking = State()
