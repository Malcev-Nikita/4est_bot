from aiogram import Dispatcher, types
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import menu_kb, register_kb, task_kb, complete_kb
from .functions import delete_call_messages 
from .config import bot

async def tasks_today(call: types.CallbackQuery):

    await delete_call_messages(call)
    DB = DataBase()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    nickname = DB.SQL(f"SELECT `nickname` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
    report = DB.SQL(f"SELECT `date`, `nickname`, `tasks` FROM `report` WHERE `date` = '{formated_date}'")

    if (len(report) != 0 and report[0][1] != nickname[0][0]):
        await call.message.answer("Сегодня уже смена открыта")

    else:
        tasks = []

        res = DB.SQL(f"SELECT `everyday_tasks`, `nickname` FROM `users` WHERE `telegram_id` = {call.from_user.id}")

        if (len(DB.SQL(f"SELECT * FROM `report` WHERE `date` = '{formated_date}' AND `nickname` = '{res[0][1]}'")) == 0):

            DB.SQL(f"INSERT INTO `report`(`date`, `nickname`, `tasks`) VALUES ('{formated_date}','{res[0][1]}', '{nickname[0][0]} - Открыл смену в {now.hour}:{now.minute}')")

            admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")
            
            for admin in admins:
                await bot.send_message(admin[0], f"{nickname[0][0]} - Открыл смену в {now.hour}:{now.minute}")


        tasks_str = res[0][0]

        tasks = tasks_str.split(', ')
        i = 0

        await call.message.answer("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n ✍️ <b>ЗАДАЧИ НА ДЕНЬ</b>\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

        while i < len(tasks):
            if ('трансфера' in tasks[i]):
                await call.message.answer('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n ✍️ <b>ЗАДАЧИ НА СЕАНС ТАТУИРОВКИ</b>\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

            await call.message.answer(f"❗️ {tasks[i]}", reply_markup = task_kb)
            i += 1


async def menu_handler(call: types.CallbackQuery):

    await delete_call_messages(call)

    telegram_id = call.from_user.id

    DB = DataBase()
    res = DB.SQL(f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}")

    if (len(res) == 0):
        await call.message.answer('Ты ещё не зарегистрировался', reply_markup = register_kb)

    else:
        await call.message.answer('Меню', reply_markup = menu_kb)


async def confirm_task(call: types.CallbackQuery):

    DB = DataBase()
    admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")
    nickname = DB.SQL(f"SELECT `nickname` FROM `users` WHERE `telegram_id` = {call.from_user.id}")

    now = datetime.now()
    
    await call.answer(cache_time=2)
    await call.message.edit_text('✅ ' + call.message.text[2:], reply_markup = complete_kb)
            
    for admin in admins:
        await bot.send_message(admin[0], f"{nickname[0][0]} - Сделал ... <b>{call.message.text[2:]}</b> ... в {now.hour}:{now.minute}")


def register_handlers_call_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(tasks_today, lambda call: call.data == 'tasks_today', state = '*')
    dp.register_callback_query_handler(menu_handler, lambda call: call.data == 'menu', state = '*')
    dp.register_callback_query_handler(confirm_task, lambda call: call.data == 'confirm', state = '*')