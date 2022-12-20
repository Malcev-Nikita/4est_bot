from .config import bot

async def delete_messages(message):

    try:
        i = 0

        while message.message_id - i:

            await bot.delete_message(message.chat.id, message.message_id - i)
            i += 1

    except:
        pass

    
async def delete_call_messages(call):

    try:
        i = 0

        while call.message.message_id - i:

            await bot.delete_message(call.message.chat.id, call.message.message_id - i)
            i += 1

    except:
        pass