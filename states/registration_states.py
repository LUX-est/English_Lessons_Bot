# states/registration_states.py
from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    name = State()
    age = State()
    level = State()
    goal_time = State()
    tutor_importance = State()
    strong_sides = State()
    weekly_lessons = State()
    format = State()
    topics = State()
    schedule = State()
    vpn = State()
    wishes = State()
