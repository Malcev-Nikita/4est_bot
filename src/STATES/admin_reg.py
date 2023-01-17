from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..CLASS.DataBase import DataBase
from ..functions import delete_messages, delete_call_messages
from ..config import code_admin


class unregistered_user(StatesGroup):
    password = State()


async def start_admin_reg(call: types.CallbackQuery, state: FSMContext):

    await delete_call_messages(call)

    await call.message.answer("Введи пароль для доступа к админке")

    await state.set_state(unregistered_user.password.state)


async def password(message: types.Message, state: FSMContext):

    await delete_messages(message)

    DB = DataBase()
    DB.SQL(f"UPDATE `users` SET `role`='admin', `everyday_tasks`='' WHERE `telegram_id` = {message.from_user.id}")

    await message.answer("<b>Отлично!</b> Тепрь ты Хозяин")

    await state.finish()

def register_handlers_admin_reg(dp: Dispatcher):
    dp.register_callback_query_handler(start_admin_reg, lambda call: call.data == 'admin', state = '*')
    dp.register_message_handler(password, lambda message: message.text == code_admin, state = unregistered_user.password)