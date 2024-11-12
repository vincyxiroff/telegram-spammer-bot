from aiogram import Bot, Dispatcher, types
import logging
import sqlite3
import nest_asyncio
nest_asyncio.apply()
import asyncio
import aiogram
import os
from config import Config
import db
import send
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
config = Config()

conn = sqlite3.connect(os.path.join('db', 'script.db'))
cursor = conn.cursor()

bot_help = """Справка по командам

!!Символы <> использованы в примерах для удобства, их ставить не надо!!

Пример добавления групп в рассылку:

/add_groups <ссылка_на_группу>
<ссылка_на_группу>
<ссылка_на_группу>

Ссылки разделены переносом строки (Shift + Enter на компьютере)
---------------------------------------------------------------

Пример удаления групп из рассылки:

/delete_groups <ссылка_на_группу>
<ссылка_на_группу>
<ссылка_на_группу>

Ссылки разделены так же, как и при добавлении
---------------------------------------------------------------

Пример добавления сообщения для рассылки:

/set_message <ваше сообщение,
сообщение, всё ещё ваше сообщение>

Сообщение задаётся просто через пробел после команды
---------------------------------------------------------------"""



bot_commands = {
    '/add_groups' : 'Добавить группы в рассылку',
    '/show_groups' : 'Показать, какие группы сейчас в рассылке',
    '/set_message' : 'Установить новый текст для рассылки',
    '/show_message' : 'Показать текущий текст рассылки',
    '/send_all' : 'Начать рассылку',
    '/delete_groups' : 'Удалить группы из рассылки',
    '/help' : 'Справка по командам'
}






bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message : types.Message):

    """Start command for bot. Greets user and shows available commands"""

    answer_message = "Привет! Вот мои команды: \n\n" +\
                        '\n'.join([f'{com} : {bot_commands[com]}' for com in bot_commands.keys()])
    await message.answer(answer_message)


@dp.message(Command("add_groups"))
async def add_groups(message: types.Message):
    """Command for adding groups to a spam-list"""

    args = message.text.split(maxsplit=1)  # Divide il testo dopo il comando
    if len(args) > 1:
        links_to_add = args[1]  # Prende il resto del testo come argomenti
        try:
            db.insert('links', links_to_add)
        except Exception as e:
            await message.answer("Не удалось записать группы\nОшибка: " + str(e))
            return
    else:
        await message.answer("Вы не написали группы!")
        return
    
    await message.answer("Группы были записаны")
    await show_groups(message)

@dp.message(Command("show_groups"))
async def show_groups(message : types.Message):

    """Command for showing user current groups in a spam-list"""

    groups = db.getall('links')
    if groups:
        answer_message = "Группы для рассылки: \n\n" +\
                                    '\n'.join([str(groups.index(group) + 1)+') ' +\
                                                group for group in groups])
                                                
        await message.answer(answer_message)
    else:
        await message.answer("У вас пока нет групп для рассылки\n" \
                              "Введите /add_groups, чтобы добавить их")


@dp.message(Command("set_message"))
async def set_message(message: types.Message):
    """Comando per impostare o aggiornare un messaggio per il bot"""
    
    # Estrai il messaggio completo dopo il comando
    if " " in message.text:
        message_to_set = message.text.split(" ", 1)[1]  # Prendi tutto dopo '/set_message'
    else:
        message_to_set = ""
    
    if message_to_set:
        try:
            # Verifica se c'è già un messaggio nel database
            cursor.execute("SELECT COUNT(*) FROM messages WHERE id = 1")
            result = cursor.fetchone()

            if result[0] > 0:  # Se il messaggio esiste già, fai un update
                db.update('messages', message_to_set)
                await message.answer("Il messaggio è stato aggiornato!")
            else:  # Altrimenti inserisci il nuovo messaggio
                db.insert('messages', message_to_set)
                await message.answer("Il messaggio è stato salvato correttamente!")
        except Exception as e:
            await message.answer("Errore nel salvataggio o nell'aggiornamento del messaggio\nErrore: " + str(e))
            return
    else:
        await message.answer("Non hai scritto alcun messaggio!")
        return

@dp.message(Command("show_message"))
async def show_message(message : types.Message):

    """Command for showing user current spam-message"""

    answer_message = db.getall('messages')
    if answer_message:
        try:
            await message.answer(answer_message[0])
        except aiogram.utils.exceptions.MessageTextIsEmpty as e:
            await message.answer('Вы задали пустое сообщение!')
    else:
        await message.answer("У вас пока нет сообщения для рассылки\n" \
                              "Введите /set_message, чтобы добавить его")

@dp.message(Command("send_all"))
async def sendall(message : types.Message):

    """Command to start spam with spam-list and spam-message specified earlier"""

    groups = db.getall('links')
    text = db.getall('messages')
    if not text[0]:
        await show_message(message)
        return
    if not groups:
        await show_groups(message)
        return

    error_message = await send.start(groups, text[0])
    if error_message:
        await message.answer('Рассылка прошла с ошибками\n\n' + error_message)
        return
    await message.answer('Рассылка успешно проведена')


@dp.message(Command("delete_groups"))
async def delete_groups(message : types.Message):

    """Command for deleting specified groups from a spam-list"""

    links_to_delete = message.get_args()
    if links_to_delete:
        try:
            db.delete('links', links_to_delete)
        except Exception as e:
            await message.answer('Не удалось удалить группы\n' + f'Ошибка: {str(e)}')
            return
    else:
        await message.answer("Вы не написали группы!")
        return

    await message.answer('Группы были удалены\n')
    await show_groups(message)
    
@dp.message(Command("help"))
async def help(message : types.Message):

    """Command for showing user help message about availible commands"""
    
    await message.answer(bot_help)


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot, skip_updates=True)
    
    asyncio.run(main())
