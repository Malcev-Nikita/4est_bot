from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime

from ..CLASS.DataBase import DataBase
from ..keyboards import users_kb, confirmation_kb, admin_kb, task_type_kb, task_type_arr


class new_task(StatesGroup):
    nickname = State()
    task = State()
    calendar = State()
    task_type = State() 
    confirmation = State()


async def start_task(call: types.CallbackQuery, state: FSMContext):

    DB = DataBase()
    res = DB.SQL("SELECT nickname FROM users")
    
    global users
    users = []

    for user in res:
        users.append(user[0])

    await call.message.answer("Кому хочешь создать задачу?", reply_markup = users_kb(users))

    await state.set_state(new_task.nickname.state)


async def nickname(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(nickname = call.data)

    await state.set_state(new_task.task_type.state)

    await call.message.answer("Отлично! Я запомнил имя. Теперь введи текст задачи")


async def task_type(message: types.Message, state: FSMContext):

    await state.update_data(task = message.text)

    await state.set_state(new_task.task.state)

    await message.answer("Отлично! Теперь выбери тип задачи", reply_markup = task_type_kb)


async def calendar(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(task_type = call.data)
    
    await state.set_state(new_task.confirmation.state)


async def task(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(task_type = call.data)
    data = await state.get_data()

    await state.set_state(new_task.confirmation.state)

    await call.message.answer(f"{data['nickname']} \n{data['task']} \nТип задачи - {data['task_type']}", reply_markup = confirmation_kb)


async def confirmation(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(confirmation = call.data)
    data = await state.get_data()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()

    if (data['task_type'] == 'everyday_task'):
        res = DB.SQL(f"SELECT `everyday_tasks` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
        print(res)

        if (res[0][0] != None):
            task_update = res[0][0] + ', ' + data['task']
        else:
            task_update = data['task']

        DB.SQL(f"UPDATE `users` SET `everyday_tasks` = '{task_update}' WHERE `telegram_id` = {call.from_user.id}")

    else:
        DB.SQL(f"INSERT INTO `tasks`(`telegram_id`, `nickname`, `task`, `date`) VALUES ({call.from_user.id},'{data['nickname']}','{data['task']}', '{formated_date}')")

    await call.message.answer("Задача создана", reply_markup = admin_kb)


def register_handlers_new_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(start_task, lambda call: call.data == 'new_task', state = '*')
    dp.register_callback_query_handler(nickname, lambda call: call.data in users, state = new_task.nickname)
    dp.register_message_handler(task_type, state = new_task.task_type)
    dp.register_callback_query_handler(task, lambda call: call.data in task_type_arr, state = new_task.task)
    dp.register_callback_query_handler(confirmation, lambda call: call.data == 'confirm', state = new_task.confirmation)