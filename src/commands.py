from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .CLASS.DataBase import DataBase
from .keyboards import register_kb, menu_kb
from .functions import delete_messages 


async def start_handler(message: types.Message, state: FSMContext):

    await delete_messages(message)

    await state.reset_state()

    telegram_id = message.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await message.answer("<b>Ты ещё не зарегистрировался</b> \n\nЖми на кнопку ниже, чтобы пройти регистрацию!", reply_markup = register_kb)

    else:
        await message.answer("<b>Ты уже есть в системе.</b> \n\nМожешь нажать на кнопку ниже или воспользоваться меню комманд. \nP.S. Она находится либо внизу слева, либо внизу справа.", reply_markup = menu_kb)


async def menu_handler(message: types.Message, state: FSMContext):

    await delete_messages(message)

    await state.reset_state()

    telegram_id = message.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    else:
        await message.answer('Меню', reply_markup = menu_kb)


def commands_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state = '*')
    dp.register_message_handler(menu_handler, commands=['menu'], state = '*')

## start - Команда для того, чтобы начать диалог с ботом
## menu - Команда для того, чтобы перейти в меню бота