from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .CLASS.DataBase import DataBase
from .keyboards import register_kb, admin_kb, menu_kb


async def start_handler(message: types.Message, state: FSMContext):

    await state.reset_state()

    telegram_id = message.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    else:
        await message.answer('Ты уже есть в системе', reply_markup = menu_kb)


async def admin_handler(message: types.Message, state: FSMContext):

    await state.reset_state()

    telegram_id = message.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id} and role = 'admin'")

    if (len(res) != 0):
        await message.answer("Добро пожаловать в админ панель, наслаждайся)", reply_markup = admin_kb)

    else:
        await message.answer("Ты не являешься администратором, свяжись с программистом, если хочешь стать админом!")


async def menu_handler(message: types.Message, state: FSMContext):

    await state.reset_state()

    telegram_id = message.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    else:
        await message.answer('Меню', reply_markup = menu_kb)


def commands_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(admin_handler, commands=['admin'])
    dp.register_message_handler(menu_handler, commands=['menu'])

## start - 
## admin - 
## menu - 