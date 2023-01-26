from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from src.CLASS.DataBase import DataBase
from src.config import bot, tattoo_master, administrator, dp
from src.keyboards import role_arr

scheduler = AsyncIOScheduler()


async def admin_message_tasks():
    DB = DataBase()
    admins = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `role` = 'admin'")

    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    yesterday = datetime.now() - timedelta(days=1)
    formated_yesterday = yesterday.strftime('%Y-%m-%d')

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

    DB.SQL(f"DELETE FROM `report` WHERE `date` = '{formated_yesterday}'")


async def reminder():
    now = datetime.now()
    formated_date = now.strftime('%Y-%m-%d')

    DB = DataBase()
    shifts = DB.SQL(f"SELECT `nickname`, `role` FROM `report` WHERE `date` = '{formated_date}' AND `tasks` LIKE '%Открыл смену%'")

    for shift in shifts:
        telegram_id = DB.SQL(f"SELECT `telegram_id` FROM `users` WHERE `nickname` = '{shift[0]}'")

        count_tasks = DB.SQL(f"SELECT COUNT(*) FROM `report` WHERE `tasks` NOT LIKE '%Открыл смену%' AND `role` = '{shift[1]}' AND `date` = '{formated_date}'")

        if ((shift[1] == 'administrator' and count_tasks[0][0] < len(administrator)) or (shift[1] == 'tattoo_master' and count_tasks[0][0] < len(tattoo_master))):
            await bot.send_message(telegram_id[0][0], f"У тебя ещё есть не выполненные задачи")


def schedule_jobs():
    scheduler.add_job(admin_message_tasks, 'cron', hour = 22 - 1, minute = 0, timezone = "Europe/Moscow")
    scheduler.add_job(reminder, 'interval', hours = 1, start_date='2023-1-1 09:00:00', end_date='2100-1-1 20:00:00', timezone = "Europe/Moscow")


async def on_sturtup(dp):
    schedule_jobs()