from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = '7542223250:AAFy0jX2bAMBQjxS2KOuIA-DvHkY526iVfk'

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обычная клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1, button2)

# Inline клавиатура
inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(inline_button1, inline_button2)

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: CallbackQuery):
    formula = '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
    await call.message.answer(formula)

@dp.callback_query_handler(text='calories')
async def set_age(call: CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий {result}')
    await state.finish()

@dp.message_handler()
async def all_messages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
