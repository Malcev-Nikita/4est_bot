from aiogram import Dispatcher, types
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import menu_kb, register_kb
from .config import date_everyday_task
from .functions import delete_call_messages 

async def tasks_today(call: types.CallbackQuery):

    await delete_call_messages(call)

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    tasks = []

    DB = DataBase()
    res1 = DB.SQL(f"SELECT `everyday_tasks` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
    res2 = DB.SQL(f"SELECT `task`, `performed` FROM `tasks` WHERE `telegram_id` = {call.from_user.id} AND `date` = '{formated_date}'")

    res = res1[0][0]
    performed = ''

    for task in res2:
        if task[1]: performed = '✅'
        else: performed = '🚫'
        
        res += ', ' + performed + ' ' + task[0]

    tasks = res.split(', ')

    await call.message.answer(f"<b>Задачи на сегодня</b> \n\n" + '\n'.join(str(value) for value in tasks))


async def menu_handler(call: types.CallbackQuery):

    await delete_call_messages(call)

    telegram_id = call.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await call.message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    else:
        await call.message.answer('Меню', reply_markup = menu_kb)


def register_handlers_call_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(tasks_today, lambda call: call.data == 'tasks_today', state = '*')
    dp.register_callback_query_handler(menu_handler, lambda call: call.data == 'menu', state = '*')