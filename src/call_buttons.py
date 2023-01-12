from aiogram import Dispatcher, types
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import menu_kb, register_kb, task_kb, complete_kb, role_arr
from .functions import delete_call_messages 
from .config import bot, tattoo_master, administrator

async def tasks_today(call: types.CallbackQuery):

    await delete_call_messages(call)
    DB = DataBase()

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    nickname = DB.SQL(f"SELECT `nickname`, `role` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
    report = DB.SQL(f"SELECT `date`, `nickname`, `tasks` FROM `report` WHERE `date` = '{formated_date}'")
    
    if (nickname[0][1] in role_arr):

        if (len(report) != 0 and report[0][1] != nickname[0][0]):
            
            role_report = DB.SQL(f"SELECT `role` FROM `users` WHERE `nickname` = '{report[0][1]}'")
            if (role_report[0][0] == nickname[0][1]): 
                await call.message.answer("Сегодня уже смена открыта")

            else: await task_today_else(call, nickname)
            
        else:
            await task_today_else(call, nickname)

    else: 
        await call.message.answer("С твоей ролью нельзя открыть смену")


async def task_today_else(call: types.CallbackQuery, nickname):

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()

    tasks = []

    res = DB.SQL(f"SELECT `everyday_tasks`, `nickname`, `role` FROM `users` WHERE `telegram_id` = {call.from_user.id}")
    tasks_completely = DB.SQL(f"SELECT `tasks` FROM `report` WHERE `date` = '{formated_date}' AND `role` = '{res[0][2]}'")

    if (len(DB.SQL(f"SELECT * FROM `report` WHERE `date` = '{formated_date}' AND `nickname` = '{res[0][1]}'")) == 0):

        DB.SQL(f"INSERT INTO `report`(`date`, `nickname`, `role`, `tasks`) VALUES ('{formated_date}','{res[0][1]}', '{nickname[0][1]}','{nickname[0][0]} - Открыл смену в {now.hour}:{now.minute}')")

        admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")
        
        for admin in admins:
            await bot.send_message(admin[0], f"{nickname[0][0]} - Открыл смену в {now.hour}:{now.minute}")


    tasks_str = res[0][0]

    tasks = tasks_str.split('; ')
    i = 0

    separator = '- ' * 35

    await call.message.answer(f"{separator}\n ✍️ <b>ЗАДАЧИ НА ДЕНЬ</b>\n{separator}")

    while i < len(tasks):

        done = False

        if (nickname[0][1] == 'tattoo_master'):
            if ('Залей сторис, перевод трансфера, к себе в сторис, в инсту и вк (Попроси админа снять на твой телефон)' in tasks[i]):
                await call.message.answer(f"{separator}\n ✍️ <b>ЗАДАЧИ НА СЕАНС ТАТУИРОВКИ</b>\n{separator}")
        
        elif (nickname[0][1] == 'administrator'):
            if ('Сторис, акция, эскизы от мастера (инста и вк)' in tasks[i]):
                await call.message.answer(f"{separator}\n ✍️ <b>СТОРИС В ТЕЧЕНИИ ДНЯ</b>\n{separator}")

            if ('Предложить клиенту чай или кофе' in tasks[i]):
                await call.message.answer(f"{separator}\n ✍️ <b>РАБОТА С КЛИЕНТОМ</b>\n{separator}")

        
        for task_completely in tasks_completely:
            if (task_completely[0] == tasks[i]): 
                done = True
                break

        if (done):
            await call.message.answer(f'✅ {tasks[i]}', reply_markup = complete_kb)

        else:
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
    nickname = DB.SQL(f"SELECT `nickname`, `role` FROM `users` WHERE `telegram_id` = {call.from_user.id}")

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')
    
    await call.answer(cache_time=2)
    await call.message.edit_text(f'✅ {call.message.text[2:]}', reply_markup = complete_kb)

    DB.SQL(f"INSERT INTO `report`(`date`, `nickname`, `role`, `tasks`) VALUES ('{formated_date}','{nickname[0][0]}','{nickname[0][1]}','{call.message.text[3:]}')")

    for admin in admins:
        await bot.send_message(admin[0], f"{nickname[0][0]} - Сделал ... <b>{call.message.text[3:]}</b> ... в {now.hour}:{now.minute}")


async def select_role(call: types.CallbackQuery):

    await delete_call_messages(call)
    
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
    DB.SQL(f"UPDATE `users` SET `role`='{call.data}',`everyday_tasks`='{tasks}' WHERE `telegram_id` = {call.from_user.id}")

    await call.message.answer("Ты выбрал роль, теперь можешь открыть смену", reply_markup = menu_kb)


def register_handlers_call_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(tasks_today, lambda call: call.data == 'tasks_today', state = '*')
    dp.register_callback_query_handler(menu_handler, lambda call: call.data == 'menu', state = '*')
    dp.register_callback_query_handler(confirm_task, lambda call: call.data == 'confirm', state = '*')
    dp.register_callback_query_handler(select_role, lambda call: call.data in role_arr)