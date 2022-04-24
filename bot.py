from aiogram import Bot, Dispatcher, executor, types
import logging
import asyncio

import aiogram
from requests import session
from config import Config
import db
from send import Send

logging.basicConfig(level=logging.INFO)
config = Config()

bot_commands = {
    '/add_groups' : 'Добавить группы в рассылку',
    '/show_groups' : 'Показать, какие группы сейчас в рассылке',
    '/set_message' : 'Установить новый текст для рассылки',
    '/show_message' : 'Показать текущий текст рассылки',
    '/send_all' : ' Начать рассылку'
}

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message : types.Message):

    """Start command for bot. Greets user and shows available commands"""

    answer_message = "Привет! Вот мои команды: \n\n" +\
                        '\n'.join([f'{com} : {bot_commands[com]}' for com in bot_commands.keys()])
    await message.answer(answer_message)


@dp.message_handler(commands=['add_groups'])
async def add_groups(message : types.Message):
    try:
        db.insert('links', message.get_args())
    except Exception as e:
        await message.answer("Не удалось записать группы\nОшибка: " + str(e))
        return
    
    await message.answer("Группы были записаны")


@dp.message_handler(commands=['show_groups'])
async def show_groups(message : types.Message):
    groups = db.getall('links')
    if groups:
        answer_message = "Группы для рассылки: \n\n" + '\n'.join([group for group in groups])
        await message.answer(answer_message)
    else:
        await message.answer("У вас пока нет групп для рассылки\n" \
                              "Введите /add_groups, чтобы добавить их")


@dp.message_handler(commands=['set_message'])
async def set_message(message : types.Message):
    messages = db.getall('messages')
    if messages:
        try:
            db.update('messages', message.get_args())
        except Exception as e:
            await message.answer("Не удалось записать сообщение\nОшибка: " + str(e))
            return
        await message.answer("Сообщение было обновлено")
        return
    db.insert('messages', message.get_args())
    await message.answer("Сообщение было записано")


@dp.message_handler(commands=['show_message'])
async def show_message(message : types.Message):
    answer_message = db.getall('messages')
    if answer_message:
        try:
            await message.answer(answer_message[0])
        except aiogram.utils.exceptions.MessageTextIsEmpty as e:
            await message.answer('Вы задали пустое сообщение!')
    else:
        await message.answer("У вас пока нет сообщения для рассылки\n" \
                              "Введите /set_message, чтобы добавить его")

@dp.message_handler(commands=['send_all'])
async def sendall(message : types.Message):
    spam = Send(config.API_ID, config.API_HASH)
    groups = db.getall('links')
    text = db.getall('messages')
    print(groups, text)
    async with spam.client.session as sess:
        await spam.start(groups, text[0])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)