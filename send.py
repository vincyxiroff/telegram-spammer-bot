from telethon import TelegramClient
import logging
from config import Config
from typing import Dict


config = Config()

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

client = TelegramClient('script', api_id=config.API_ID, api_hash=config.API_HASH)

async def sendall(groups, message_text):
    errors = {}
    for group in groups:
        try:
            await client.send_message(group, message_text)
        except Exception as e:
            errors[f'{group}'] = str(e)
    return errors

async def create_error_message(errors : Dict):
    answer_message = ''
    for i, (error_group, error_message) in enumerate(errors.items()):
        answer_message += f"Не удалось отправить сообщение в группу {error_group}\n"\
                   f"Ошибка: {error_message}\n\n"

    return answer_message

async def start(groups, message_text):
    async with client:
        errors = client.loop.run_until_complete(sendall(groups, message_text))
        return await create_error_message(errors)
