from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types



TOKEN         = "6167962615:AAE89WBo_c3ewtw0n2hpHrs8UA9QbYaa2Wg" # Тест
# TOKEN         = "5986825673:AAEVQNsig6A-QsMjZj_piIQ_n60M3Mc8yh0" # Не тест

STORAGE       = MemoryStorage()

bot           = Bot(token=TOKEN, parse_mode = types.ParseMode.HTML)
dp            = Dispatcher(bot, storage=STORAGE)

HOST          = '92.53.105.154'
USER          = 'gen_user'
PASSWD        = '3w2S6xi3fTVZnRR'
DB            = 'default_db'

tattoo_master_everyday = [ 'Фото с собой и приветствие (вк, инст, вотс)',
                           'Акция (эскиз, пинтерест и т.д.) без слова акция и скидка (вк, инст, вотс)',
                           'Твоё тату (фото, видео) (вк, инст, вотс)',
                           'Рассылка Инст - 20шт, Вк - 15шт',
                           'Пост со своей тату (вк, инст, вотс)' ]

code_admin    = 'Честь'