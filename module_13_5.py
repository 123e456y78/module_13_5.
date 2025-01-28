from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
api = '7314899914:AAHcsc1SyUJccc3bK3jNxYvAkCdAfC8fxas'
bot = Bot(token=api)
dp = Dispatcher()
router = Router()
dp.include_router(router)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]], resize_keyboard=True)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
def is_valid_number(value):
    return value.isdigit() and int(value) > 0
@router.message(F.text.lower() == 'рассчитать')
async def set_age(message: types.Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)
@router.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(age=int(message.text))
        await message.answer("Введите свой рост (в см):")
        await state.set_state(UserState.growth)
    else:
        await message.answer("Возраст должен быть положительным числом. Пожалуйста, введите корректное значение.")
@router.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(growth=int(message.text))
        await message.answer("Введите свой вес (в кг):")
        await state.set_state(UserState.weight)
    else:
        await message.answer("Рост должен быть положительным числом. Пожалуйста, введите корректное значение.")
@router.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(weight=int(message.text))
        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")
        await state.clear()
    else:
        await message.answer("Вес должен быть положительным числом. Пожалуйста, введите корректное значение.")

@dp.message(Command("start"))
async def start_form(message: Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Если хочешь узнать свою суточную норму "
                         "калорий, то нажми 'Рассчитать'.", reply_markup=kb)
@router.message(~F.text.lower('Рассчитать') and ~F.state(UserState.age) and ~F.state(UserState.growth)
                and ~F.state(UserState.weight))
async def redirect_to_start(message: types.Message):
    await start_form(message)
async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())