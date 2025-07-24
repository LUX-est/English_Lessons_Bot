# handlers/user/registration.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.registration_states import RegistrationStates
from keyboards.reply import get_main_menu
from database.models import User
from database.db import get_db
from sqlalchemy import select
from aiogram.filters.command import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with get_db() as session:
        result = await session.execute(select(User).where(User.tg_id == user_id))
        user = result.scalars().first()
    if user:
        await message.answer(
            f"👋 Привет, <b>{user.name}</b>! Рады видеть тебя снова!",
            reply_markup=get_main_menu()
        )
        await state.clear()
    else:
        await message.answer("Привет! Чтобы начать, пожалуйста, пройди регистрацию.\n\nКак тебя зовут?")
        await state.set_state(RegistrationStates.name)

@router.message(RegistrationStates.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(RegistrationStates.age)

@router.message(RegistrationStates.age)
async def reg_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Как вы оцените свой текущий уровень английского?")
    await state.set_state(RegistrationStates.level)

@router.message(RegistrationStates.level)
async def reg_level(message: Message, state: FSMContext):
    await state.update_data(level=message.text)
    await message.answer("В какой срок вы бы хотели уложиться для достижения своей цели?")
    await state.set_state(RegistrationStates.goal_time)

@router.message(RegistrationStates.goal_time)
async def reg_goal(message: Message, state: FSMContext):
    await state.update_data(goal_time=message.text)
    await message.answer("Что для вас самое важное в репетиторе по английскому?")
    await state.set_state(RegistrationStates.tutor_importance)

@router.message(RegistrationStates.tutor_importance)
async def reg_importance(message: Message, state: FSMContext):
    await state.update_data(tutor_importance=message.text)
    await message.answer("Какие навыки вы считаете своими сильными сторонами?")
    await state.set_state(RegistrationStates.strong_sides)

@router.message(RegistrationStates.strong_sides)
async def reg_strong(message: Message, state: FSMContext):
    await state.update_data(strong_sides=message.text)
    await message.answer("Сколько раз в неделю вы хотели бы заниматься?")
    await state.set_state(RegistrationStates.weekly_lessons)

@router.message(RegistrationStates.weekly_lessons)
async def reg_weekly(message: Message, state: FSMContext):
    await state.update_data(weekly_lessons=message.text)
    await message.answer("Какой формат занятий вам наиболее удобен? (Индивидуально / в группе)")
    await state.set_state(RegistrationStates.format)

@router.message(RegistrationStates.format)
async def reg_format(message: Message, state: FSMContext):
    await state.update_data(format=message.text)
    await message.answer("Есть ли конкретные темы или сферы, которые вам интересны?")
    await state.set_state(RegistrationStates.topics)

@router.message(RegistrationStates.topics)
async def reg_topics(message: Message, state: FSMContext):
    await state.update_data(topics=message.text)
    await message.answer("В какие дни и время вам удобнее заниматься?")
    await state.set_state(RegistrationStates.schedule)

@router.message(RegistrationStates.schedule)
async def reg_schedule(message: Message, state: FSMContext):
    await state.update_data(schedule=message.text)
    await message.answer("Есть ли у вас доступ к VPN?")
    await state.set_state(RegistrationStates.vpn)

@router.message(RegistrationStates.vpn)
async def reg_vpn(message: Message, state: FSMContext):
    await state.update_data(vpn=message.text)
    await message.answer("Особые пожелания по обучению?")
    await state.set_state(RegistrationStates.wishes)

@router.message(RegistrationStates.wishes)
async def reg_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    async with get_db() as session:
        result = await session.execute(select(User).where(User.tg_id == message.from_user.id))
        user_exists = result.scalars().first()
        if user_exists:
            user_exists.name = data.get("name")
            user_exists.age = data.get("age")
            user_exists.level = data.get("level")
            user_exists.goal_time = data.get("goal_time")
            user_exists.tutor_importance = data.get("tutor_importance")
            user_exists.strong_sides = data.get("strong_sides")
            user_exists.weekly_lessons = data.get("weekly_lessons")
            user_exists.format = data.get("format")
            user_exists.topics = data.get("topics")
            user_exists.schedule = data.get("schedule")
            user_exists.vpn = data.get("vpn")
            user_exists.wishes = data.get("wishes")
        else:
            user = User(
                tg_id=message.from_user.id,
                name=data.get("name"),
                age=data.get("age"),
                level=data.get("level"),
                goal_time=data.get("goal_time"),
                tutor_importance=data.get("tutor_importance"),
                strong_sides=data.get("strong_sides"),
                weekly_lessons=data.get("weekly_lessons"),
                format=data.get("format"),
                topics=data.get("topics"),
                schedule=data.get("schedule"),
                vpn=data.get("vpn"),
                wishes=data.get("wishes")
            )
            session.add(user)
        await session.commit()
    await message.answer("✅ Регистрация завершена!", reply_markup=get_main_menu())
    await state.clear()
