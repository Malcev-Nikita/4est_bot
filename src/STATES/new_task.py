from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime

from ..CLASS.DataBase import DataBase
from ..keyboards import users_kb, confirmation_kb, admin_kb


users = []

class new_task(StatesGroup):
    nickname = State()
    task = State()
    confirmation = State()


async def start_task(call: types.CallbackQuery, state: FSMContext):

    DB = DataBase()
    res = DB.SQL("SELECT nickname FROM users")
    
    for user in res:
        users.append(user[0])

    await call.message.answer("Кому хочешь создать задачу?", reply_markup = users_kb(users))

    await state.set_state(new_task.nickname.state)


async def nickname(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(nickname = call.data)

    await state.set_state(new_task.task.state)

    await call.message.answer("Отлично! Я запомнил имя. Теперь введи текст задачи")


async def task(message: types.Message, state: FSMContext):

    await state.update_data(task = message.text)
    data = await state.get_data()

    await state.set_state(new_task.confirmation.state)

    await message.answer(f"{data['nickname']} \n{data['task']}", reply_markup = confirmation_kb)


async def confirmation(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(confirmation = call.data)
    data = await state.get_data()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()
    DB.SQL(f"INSERT INTO `tasks`(`telegram_id`, `nickname`, `task`, `date`) VALUES ('{call.from_user.id}','{data['nickname']}','{data['task']}', '{formated_date}')")

    await call.message.answer("Задача создана", reply_markup = admin_kb)



## Регистрируем обработчики событий ############################################
def register_handlers_new_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(start_task, lambda call: call.data == 'new_task', state = '*')
    dp.register_callback_query_handler(nickname, lambda call: call.data in users, state = new_task.nickname)
    dp.register_message_handler(task, state = new_task.task)
    dp.register_callback_query_handler(confirmation, lambda call: call.data == 'confirm', state = new_task.confirmation)