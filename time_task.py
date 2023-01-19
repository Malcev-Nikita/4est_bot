from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio
from aiogram import executor
import schedule
from datetime import datetime

from src.CLASS.DataBase import DataBase
from src.config import bot, tattoo_master, administrator, dp
from src.keyboards import role_arr

scheduler = AsyncIOScheduler()


async def outstanding_tasks():
    DB = DataBase()
    admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    separator = '- ' * 22

    for role in role_arr:
        res = DB.SQL(f"SELECT `tasks` FROM `report` WHERE `date` = '{formated_date}' AND `role` = '{role}'")
        
        tasks = []
        for task in res:
            tasks.append(task[0])

        tasks_str = '; '.join(tasks)

        for admin in admins:
            if (role == 'tattoo_master'):
                await bot.send_message(admin[0], f"{separator}\n ✍️ <b>Тату мастер</b>\n{separator}")

                for task_tattoo_master in tattoo_master:
                    if (task_tattoo_master not in tasks_str):
                        await bot.send_message(admin[0], f"🚫 Тату мастер не сделал ... <b>{task_tattoo_master}</b>")


            elif (role == 'administrator'):
                await bot.send_message(admin[0], f"{separator}\n ✍️ <b>Администратор</b>\n{separator}")

                for task_administrator in administrator:
                    if (task_administrator not in tasks_str):
                        await bot.send_message(admin[0], f"🚫 Администратор не сделал ... <b>{task_administrator}</b>")



def schedule_jobs():
    scheduler.add_job(outstanding_tasks, 'cron', hour = 21 - 1, minute = 0, timezone = "Europe/Moscow")

async def on_sturtup(dp):
    schedule_jobs()

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup = on_sturtup)