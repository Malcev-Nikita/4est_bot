from aiogram import Dispatcher, types
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import calendar_kb, button_calendar_arr
from .config import date_new_task_user
from .functions import delete_call_messages 

async def tasks_today(call: types.CallbackQuery):

    await delete_call_messages(call)

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    tasks = []

    DB = DataBase()
    res1 = DB.SQL(f"SELECT `everyday_tasks` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
    res2 = DB.SQL(f"SELECT `task` FROM `tasks` WHERE `telegram_id` = {call.from_user.id} AND `date` = '{formated_date}' AND `performed` = false")

    res = res1[0][0]
    
    for task in res2:
        res += ', ' + task[0]

    tasks = res.split(', ')

    await call.message.answer(f"<b>Задачи на сегодня</b> \n\n" + '\n'.join(str(value) for value in tasks))


async def new_task_me(call: types.CallbackQuery):

    await delete_call_messages(call)

    current_datetime = datetime.now()

    date_new_task_user[call.from_user.id] = [current_datetime.year, current_datetime.month]

    await call.message.answer("Выбери дату на которую хочешь создать задание", reply_markup = calendar_kb(date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1]))


async def new_task_me_button(call: types.CallbackQuery):

    await delete_call_messages(call)

    if (call.data == 'next'):
        if (date_new_task_user.get(call.from_user.id)[1] == 12): date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0] + 1, 0]

        date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1] + 1]
    
    elif (call.data == 'back'):
        if (date_new_task_user.get(call.from_user.id)[1] == 1): date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0] - 1, 13]

        date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1] - 1]

    await call.message.answer("Выбери дату на которую хочешь создать задание", reply_markup = calendar_kb(date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1]))

def register_handlers_call_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(tasks_today, lambda call: call.data == 'tasks_today', state = '*')
    dp.register_callback_query_handler(new_task_me, lambda call: call.data == 'new_task_me', state = '*')
    dp.register_callback_query_handler(new_task_me_button, lambda call: call.data in button_calendar_arr, state = '*')