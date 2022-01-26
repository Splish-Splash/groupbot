from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import Query
from config import TOKEN
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

current_queries = []

button_hi = KeyboardButton('Hiiiiiii')
new_kb = ReplyKeyboardMarkup(resize_keyboard=True)
new_kb.add(button_hi)

current_msg = []

with open('history.txt', 'r') as f:
    l = f.readlines()
    for i in range(0, len(l), 2):
        cid, mid = l[i].split()
        query = l[i+1].split()
        current_queries.append(Query(' '.join(query[:-25]) + ' ', query[-25:]))
        current_msg.append((cid, mid))

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("debil")


# @dp.message_handler()
# async def echo_message(message: types.Message):
#     await bot.send_message(message.from_user.id, message.text)


@dp.message_handler(commands=['new'])
async def new_query(message: types.Message):
    name = message.text[5:] + ' '
    if len(name) < 3:
        msg = await bot.send_message(message.chat.id, 'Нужно написать название очереди после /new')
        return
    for q in current_queries:
        if name == q.name:
            await bot.send_message(message.chat.id, 'Очередь с таким именем уже существует')
            return
    current_queries.append(Query(name))
    new_kb = InlineKeyboardMarkup()
    for i in range(0, 25, 5):
        new_kb.row(InlineKeyboardButton(str(i+1), callback_data=name+str(i+1)), InlineKeyboardButton(str(i+2), callback_data=name+str(i+2)),
                   InlineKeyboardButton(str(i+3), callback_data=name+str(i+3)), InlineKeyboardButton(str(i+4), callback_data=name+str(i+4)),
                   InlineKeyboardButton(str(i+5), callback_data=name+str(i+5)))
    #current_kb.append(new_kb)
    msg = await bot.send_message(message.chat.id, current_queries[-1], reply_markup=new_kb)
    print(msg)
    current_msg.append((msg.chat.id, msg.message_id))
    with open('history.txt', 'w') as f:
        for i in range(len(current_msg)):
            f.write(f'{current_msg[i][0]} {current_msg[i][1]} \n')
            f.write(f'{current_queries[i].name} {" ".join(map(str, current_queries[i].query))} \n')
            #f.write(' '.join(map(str, current_queries[i].query)))

@dp.callback_query_handler(lambda c: c.data)
async def button_click(callback_query: types.CallbackQuery):
    name = ' '.join(callback_query.data.split()[:-1]) + ' '

    id = int(callback_query.data.split()[-1])
    query = find_query(name)
    query.set(id, callback_query.from_user.username)
    num = current_queries.index(query)
    new_kb = InlineKeyboardMarkup()
    for i in range(0, 25, 5):
        new_kb.row(InlineKeyboardButton(str(i + 1), callback_data=name + str(i + 1)),
                   InlineKeyboardButton(str(i + 2), callback_data=name + str(i + 2)),
                   InlineKeyboardButton(str(i + 3), callback_data=name + str(i + 3)),
                   InlineKeyboardButton(str(i + 4), callback_data=name + str(i + 4)),
                   InlineKeyboardButton(str(i + 5), callback_data=name + str(i + 5)))
    await edit_msg2(current_msg[num], query, new_kb)


# async def edit_msg(message: types.Message, query: Query):
#     if message.text != str(query):
#         await message.edit_text(query, reply_markup=message.reply_markup)


async def edit_msg2(msg, query: Query, new_kb):
    #mssg = await bot.stop_message_live_location(msg[0], msg[1])
    #mssg = await bot.edit_message_media(None, msg[0], msg[1])
    #mssg = await bot.edit_message_caption(msg[0], msg[1])
    await bot.edit_message_text(query, msg[0], msg[1], reply_markup=new_kb)
    #types.chat.Chat.get


def find_query(name):
    for q in current_queries:
        if q.name == name:
            return q

if __name__ == '__main__':
    executor.start_polling(dp)