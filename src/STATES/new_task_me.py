from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime

from ..CLASS.DataBase import DataBase
from ..keyboards import users_kb, confirmation_kb, admin_kb, task_type_kb, task_type_arr
from ..functions import delete_messages, delete_call_messages
from ..keyboards import calendar_kb
from ..config import date_new_task_user


class new_task_me(StatesGroup):
    task = State()
    calendar = State()
    task_type = State() 
    confirmation = State()


async def start_task(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    await state.set_state(new_task_me.task_type.state)

    await call.message.answer("Введи текст задачи")


async def task_type(message: types.Message, state: FSMContext):

    await delete_messages(message)

    await state.update_data(task = message.text)

    await state.set_state(new_task_me.task.state)

    await message.answer("<b>Отлично!</b> \n\nТеперь выбери тип задачи", reply_markup = task_type_kb)


async def calendar(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    await state.set_state(new_task_me.task.state)

    if (call.data == "date_task"):
        await state.update_data(task_type = call.data)

        current_datetime = datetime.now()

        date_new_task_user[call.from_user.id] = [current_datetime.year, current_datetime.month]

    elif (call.data == "next" or call.data == "back"):
        if (call.data == 'next'):
            if (date_new_task_user.get(call.from_user.id)[1] == 12): date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0] + 1, 0]

            date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1] + 1]
    
        elif (call.data == 'back'):
            if (date_new_task_user.get(call.from_user.id)[1] == 1): date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0] - 1, 13]

            date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1] - 1]


    await call.message.answer("Выбери дату на которую хочешь создать задание", reply_markup = calendar_kb(date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1]))

async def task(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    date = "не задана"

    if (int(call.data) >= 1 and int(call.data) <= 31):
        date_new_task_user[call.from_user.id] = [date_new_task_user.get(call.from_user.id)[0], date_new_task_user.get(call.from_user.id)[1] - 1, call.data]

        await state.update_data(task_type = "calendar")

        date = f"{date_new_task_user.get(call.from_user.id)[2]}.{date_new_task_user.get(call.from_user.id)[1] + 1}.{date_new_task_user.get(call.from_user.id)[0]}"

    else: 
        await state.update_data(task_type = call.data)

    data = await state.get_data()

    await state.set_state(new_task_me.confirmation.state)

    await call.message.answer(f"{data['task']} \nТип задачи - {data['task_type']} \nДата - {date}", reply_markup = confirmation_kb)


async def confirmation(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    await state.update_data(confirmation = call.data)
    data = await state.get_data()

    DB = DataBase()
    nickname = DB.SQL(f"SELECT `nickname` FROM `users` WHERE `telegram_id` = '{call.from_user.id}'")

    if (data['task_type'] == 'everyday_task'):
        res = DB.SQL(f"SELECT `everyday_tasks` FROM `users` WHERE `telegram_id` = {call.from_user.id}")

        if (res[0][0] != None):
            task_update = res[0][0] + ', ' + data['task']
        else:
            task_update = data['task']

        DB.SQL(f"UPDATE `users` SET `everyday_tasks` = '{task_update}' WHERE `telegram_id` = {call.from_user.id}")

    else:
        DB.SQL(f"INSERT INTO `tasks`(`telegram_id`, `nickname`, `task`, `date`) VALUES ({call.from_user.id},'{nickname[0][0]}','{data['task']}', '{date_new_task_user.get(call.from_user.id)[0]}-{date_new_task_user.get(call.from_user.id)[1] + 1}-{date_new_task_user.get(call.from_user.id)[2]}')")
        date_new_task_user.pop(call.from_user.id)

    await call.message.answer("Задача создана", reply_markup = admin_kb)


def register_handlers_new_tasks_me(dp: Dispatcher):
    dp.register_callback_query_handler(start_task, lambda call: call.data == 'new_task_me', state = '*')
    dp.register_message_handler(task_type, state = new_task_me.task_type)
    dp.register_callback_query_handler(calendar, lambda call: call.data == "date_task" or call.data == "next" or call.data == "back", state = new_task_me.task)
    dp.register_callback_query_handler(task, lambda call: call.data == "everyday_task" or ( int(call.data) >= 1 and int(call.data) <= 31 ), state = new_task_me.task)
    dp.register_callback_query_handler(confirmation, lambda call: call.data == 'confirm', state = new_task_me.confirmation)