from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher


TOKEN = "5986825673:AAEVQNsig6A-QsMjZj_piIQ_n60M3Mc8yh0"

STORAGE = storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

HOST = 'localhost'
USER = 'root'
PASSWD = ''
DB = '4est_duty_bot'