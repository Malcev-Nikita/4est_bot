from aiogram import executor
import asyncio
import aioschedule
from datetime import datetime

from src.CLASS.DataBase import DataBase
from src.config import bot, tattoo_master, administrator, dp
from src.keyboards import role_arr


async def outstanding_tasks():
    DB = DataBase()
    admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    separator = '- ' * 22

    for role in role_arr:
        tasks = DB.SQL(f"SELECT `tasks` FROM `report` WHERE `date` = '{formated_date}' AND `role` = '{role}'")

        for admin in admins:
            await bot.send_message(f"{separator}\n ✍️ <b>Тату мастер</b>\n{separator}")

            for task in tasks: 
                i = 1
                for task_tattoo_master in tattoo_master:
                    if (task[0] != task_tattoo_master and i == len(task_tattoo_master)):
                        await bot.send_message(admin[0], f"🚫 Тату мастер не сделал ... <b>{task[0]}</b>")

                    i += 1

async def scheduler():
    aioschedule.every().day.at("1:16").do(outstanding_tasks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(): 
    await asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(on_startup)

