from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import register_kb, role_kb, role_arr, task_kb, complete_kb
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
        await message.answer("<b>Ты уже есть в системе.</b> \n\nМожешь воспользоваться меню комманд. \nP.S. Она находится либо внизу слева, либо внизу справа.")


async def open_handler(message: types.Message, state: FSMContext):

    await delete_messages(message)

    await state.reset_state()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()

    nickname = DB.SQL(f"SELECT `nickname`, `role` FROM `users` WHERE `telegram_id` = {message.from_user.id}")
    report = DB.SQL(f"SELECT `date`, `nickname`, `tasks`, `role` FROM `report` WHERE `date` = '{formated_date}' AND `role` = '{nickname[0][1]}' AND `tasks` LIKE '%Открыл смену%'")
    
    if (nickname[0][1] in role_arr):

        if (len(report) != 0 and report[0][1] != nickname[0][0]): await message.answer("Сегодня уже смена открыта")
            
        else: await task_today_else(message, nickname)

    else: 
        await message.answer("С твоей ролью нельзя открыть смену")


async def task_today_else(message: types.Message, nickname):

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()

    res = DB.SQL(f"SELECT `everyday_tasks`, `nickname`, `role` FROM `users` WHERE `telegram_id` = {message.from_user.id}")
    tasks_completely = DB.SQL(f"SELECT `tasks` FROM `report` WHERE `date` = '{formated_date}' AND `role` = '{res[0][2]}'")

    if (len(DB.SQL(f"SELECT * FROM `report` WHERE `date` = '{formated_date}' AND `nickname` = '{res[0][1]}'")) == 0):

        DB.SQL(f"INSERT INTO `report`(`date`, `nickname`, `role`, `tasks`) VALUES ('{formated_date}','{res[0][1]}', '{nickname[0][1]}','{nickname[0][0]} - Открыл смену в {now.hour}:{now.minute}')")

        admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")
        
        for admin in admins:
            await bot.send_message(admin[0], f"{nickname[0][0]} - 🚪 Открыл смену в {now.hour}:{now.minute}")


    tasks = []
    tasks = res[0][0].split('; ')
    i = 0

    separator = '- ' * 22

    await message.answer(f"{separator}\n ✍️ <b>ЗАДАЧИ НА ДЕНЬ</b>\n{separator}")

    while i < len(tasks):

        done = False

        if ('Залей сторис, перевод трансфера, к себе в сторис, в инсту и вк (Попроси админа снять на твой телефон)' == tasks[i]):
            await message.answer(f"{separator}\n ✍️ <b>ЗАДАЧИ НА СЕАНС ТАТУИРОВКИ</b>\n{separator}")
    
        if ('Сторис, акция, эскизы от мастера (инста и вк)' == tasks[i]):
            await message.answer(f"{separator}\n ✍️ <b>СТОРИС В ТЕЧЕНИИ ДНЯ</b>\n{separator}")

        if ('Предложить клиенту чай или кофе' == tasks[i]):
            await message.answer(f"{separator}\n ✍️ <b>РАБОТА С КЛИЕНТОМ</b>\n{separator}")

        
        for task_completely in tasks_completely:
            if (task_completely[0] == tasks[i]): 
                done = True
                break

        if (done): await message.answer(f'✅ {tasks[i]}', reply_markup = complete_kb)

        else: await message.answer(f"❗️ {tasks[i]}", reply_markup = task_kb)

        i += 1  


async def role_handler(message: types.Message, state: FSMContext):
    
    await delete_messages(message)

    await state.reset_state()

    await message.answer('Выбери свою роль', reply_markup = role_kb)


async def close_handler(message: types.Message, state: FSMContext):
    
    await delete_messages(message)

    await state.reset_state()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()
    nickname = DB.SQL(f"SELECT `nickname`, `role` FROM `users` WHERE `telegram_id` = {message.from_user.id}")

    if (nickname[0][1] in role_arr):
        DB.SQL(f"DELETE FROM `report` WHERE `date` = '{formated_date}' AND `nickname` = '{nickname[0][0]}' AND `tasks` LIKE '%Открыл смену%'")

        admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")

        await message.answer('Ты закрыл смену')

        for admin in admins:
            await bot.send_message(admin[0], f"{nickname[0][0]} - 🚪 Закрыл смену в {now.hour}:{now.minute}")

    else: 
        await message.answer('С твоей ролью нельзя закрыть смену')

def commands_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state = '*')
    dp.register_message_handler(open_handler, commands=['open'], state = '*')
    dp.register_message_handler(role_handler, commands=['role'], state = '*')
    dp.register_message_handler(close_handler, commands=['close'], state = '*')

## open - Открыть смену
## close - Закрыть смену
## role - Сменить роль