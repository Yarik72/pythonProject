from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from crud_functions import initiate_db, get_all_products, add_user, is_included
import asyncio


api = ''

initiate_db()
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обычная клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button1, button2, button3, button4)

# Inline клавиатура
inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(inline_button1, inline_button2)

# Inline клавиатура для продуктов
inline_kb2 = InlineKeyboardMarkup(resize_keyboard=True)
inline_button_product1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
inline_button_product2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
inline_button_product3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
inline_button_product4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
inline_kb2.add(inline_button_product1, inline_button_product2, inline_button_product3, inline_button_product4)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message: Message):
    products = get_all_products()
    for product in products:
        await message.answer(f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}")
        with open(f'{product[0]}.jpg', 'rb') as jpg:
            await message.answer_photo(jpg)
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: CallbackQuery):
    formula = '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
    await call.message.answer(formula)


@dp.message_handler(text='Регистрация')
async def sing_up(message: Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    username = message.text
    if not is_included(username):
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно!")
    await state.finish()


@dp.message_handler()
async def all_messages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
