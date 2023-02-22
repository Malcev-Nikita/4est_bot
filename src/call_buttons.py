from aiogram import Dispatcher, types
from datetime import datetime

from .CLASS.DataBase import DataBase
from .keyboards import menu_kb, register_kb, complete_kb, role_arr
from .functions import delete_call_messages 
from .config import bot, tattoo_master, administrator


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

    if call.data == 'confirm':
        for admin in admins:
            await bot.send_message(admin[0], f"{nickname[0][0]} - ✅ Сделал ... <b>{call.message.text[3:]}</b> ... в {now.hour}:{now.minute}")


async def select_role(call: types.CallbackQuery):

    await delete_call_messages(call)

    DB = DataBase()
    tasks_sql = DB.SQL(f"SELECT `id`, `name`, `description`, `type` FROM `{call.data}_tasks`")

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')
    
    tasks = ''
    
    for task in tasks_sql:
        tasks += task[2] + "; "

    tasks = tasks[:-2]
    
    DB.SQL(f"UPDATE `users` SET `role`='{call.data}',`everyday_tasks`='{tasks}' WHERE `telegram_id` = {call.from_user.id}")

    nickname = DB.SQL(f"SELECT `nickname` FROM `users` WHERE `telegram_id` = {call.from_user.id}")

    DB.SQL(f"DELETE FROM `report` WHERE `date` = '{formated_date}' AND `nickname` = '{nickname[0][0]}' AND `tasks` LIKE '%Открыл смену%'")

    await call.message.answer("Ты выбрал роль, теперь можешь открыть смену. Её можно открыть в плашке Меню")


def register_handlers_call_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(menu_handler, lambda call: call.data == 'menu', state = '*')
    dp.register_callback_query_handler(confirm_task, lambda call: call.data == 'confirm' or call.data == 'no_confirm', state = '*')
    dp.register_callback_query_handler(select_role, lambda call: call.data in role_arr)