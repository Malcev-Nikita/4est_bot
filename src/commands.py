from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import register_kb, menu_kb, role_kb
from .functions import delete_messages 
from .config import bot

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
    res = DB.SQL(f"SELECT `telegram_id`, `role` FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    elif (res[0][1] == 'exit'):
        await message.answer('У тебя не выбрана роль', reply_markup = role_kb)

    else:
        await message.answer('Меню', reply_markup = menu_kb)


async def exit_handler(message: types.Message, state: FSMContext):
    
    await delete_messages(message)

    await state.reset_state()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()
    DB.SQL(f"UPDATE `users` SET `role` = 'exit', `everyday_tasks` = '' WHERE `telegram_id` = {message.from_user.id}")

    nickname = DB.SQL(f"SELECT `nickname` FROM `users` WHERE `telegram_id` = {message.from_user.id}")

    DB.SQL(f"DELETE FROM `report` WHERE `date` = '{formated_date}' AND `nickname` = '{nickname[0][0]}'")

    

def commands_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state = '*')
    dp.register_message_handler(menu_handler, commands=['menu'], state = '*')
    dp.register_message_handler(exit_handler, commands=['exit'], state = '*')

## start - Команда для того, чтобы начать диалог с ботом
## menu - Команда для того, чтобы перейти в меню бота