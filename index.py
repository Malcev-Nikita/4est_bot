from aiogram import executor, types
from aiogram.dispatcher import FSMContext
import logging

from CLASS.DataBase import DataBase
from keyboards import register_kb
from config import dp

from STATES.unregistered_user import register_handlers_telegram_start


logging.basicConfig(level=logging.INFO)


@dp.message_handler(state = '*', commands = 'start')
async def start_handler(message: types.Message, state: FSMContext):

    await state.reset_state()

    telegram_id = message.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    else:
        await message.answer('Ты уже есть в системе')


@dp.message_handler(state = '*', commands = 'cancel')
async def cancel_handler(message: types.Message, state: FSMContext):

    await state.reset_state()

    await message.answer("Ваш прогресс сброшен")


register_handlers_telegram_start(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)