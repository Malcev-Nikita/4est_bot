from aiogram import Dispatcher, types
from datetime import datetime

from .CLASS.DataBase import DataBase

async def tasks_today(call: types.CallbackQuery):

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    tasks = []

    DB = DataBase()
    res1 = DB.SQL(f"SELECT `everyday_tasks` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
    res2 = DB.SQL(f"SELECT `task` FROM `tasks` WHERE `telegram_id` = {call.from_user.id} AND `date` = '{formated_date}' AND `performed` = false")

    if (len(res2) != 0):
        for task in res1, res2: tasks.append(task[0])
    else:
        for task in res1: tasks.append(task[0])

    res = ''
    for task in tasks:
        res += f'{task} \n'


    await call.message.answer(f"Задачи на сегодня \n{res}")


def register_handlers_call_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(tasks_today, lambda call: call.data == 'tasks_today', state = '*')