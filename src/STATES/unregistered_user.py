from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..CLASS.DataBase import DataBase
from ..keyboards import role_kb, role_arr
from ..functions import delete_messages, delete_call_messages
from ..config import tattoo_master, administrator


class unregistered_user(StatesGroup):
    nickname = State()
    role = State()


async def start_register(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    await call.message.answer("<b>Введи своё имя.</b> \n\nЭто имя будет отображаться админам бота!")

    await state.set_state(unregistered_user.nickname.state)


async def nickname(message: types.Message, state: FSMContext):

    await delete_messages(message)

    await state.update_data(nickname = message.text)

    await state.set_state(unregistered_user.role.state)

    await message.answer("<b>Отлично!</b> Я запомнил твоё имя. \n\nТеперь выбери кто ты", reply_markup = role_kb)


async def role(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    await state.update_data(role = call.data)
    data = await state.get_data()

    tasks = ''
    
    if call.data == 'tattoo_master': 
        tasks = tattoo_master[0]

        for task in tattoo_master:
            tasks += '; ' + task


    elif call.data == 'administrator': 
        tasks = administrator[0]

        for task in administrator:
            tasks += '; ' + task

    DB = DataBase()
    DB.SQL(f"INSERT INTO users (telegram_id, nickname, role, everyday_tasks) VALUES ({call.from_user.id}, '{data['nickname']}', '{data['role']}', '{tasks}')")

    await call.message.answer("<b>Отлично!</b> Ты зарегистрирован")

    await state.finish()


def register_handlers_telegram_start(dp: Dispatcher):
    dp.register_callback_query_handler(start_register, lambda call: call.data == 'register', state = '*')
    dp.register_message_handler(nickname, state = unregistered_user.nickname)
    dp.register_callback_query_handler(role, lambda call: call.data in role_arr, state = unregistered_user.role)