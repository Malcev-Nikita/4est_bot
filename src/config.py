from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types


TOKEN       = "5986825673:AAEVQNsig6A-QsMjZj_piIQ_n60M3Mc8yh0"
STORAGE     = MemoryStorage()

bot         = Bot(token=TOKEN, parse_mode = types.ParseMode.HTML)
dp          = Dispatcher(bot, storage=STORAGE)

HOST        = '92.53.105.154'
USER        = 'gen_user'
PASSWD      = '3w2S6xi3fTVZnRR'
DB          = 'default_db'

master      = 'Подобрать эскизы из интернета для сторис (постить в акк Честь и себе в инст и в вк), Нарисовать один эскиз или сделать набросок для среды (постить эскизы в акк Честь и себе), Консультация - выкладываемся на полную, Контент (качественные фото; сториc к себе всех процессов ), Фото с клиентом (Выложить в акк Честь), Попросить клиента выложить сторис с отметкой; оставить отзыв и т.д., Сделать рассылку по своим подписчикам и незнакомым людям в инст и вк'
master_time = '10:30, 1, 1, 1, 1, 16:00'
admin       = 'Заявки! Быть на чеку! Работать по схеме! (вк. инст. amoCRM. вотсап. комментарии. авито. телега), Контент инста (сторис с тату процессами. эскизы. хочешь тату. сегодня мастер. сертификаты. кредит. обучение. имидж), Контент вк (дублировать всё из инсты), Сервис (чай. кофе и т.д.), Санитария (уборка. бахилы. вёдра. и т.д.), Обратная связь (дни рождения. как заживление. напомнить о нас), Фоткать мастеров с клиентами и выкладывать в сторис!, Рассылка в инст и вк!'
admin_time  = '1, 1, 1, 1, 1, 1, 1, 1' 