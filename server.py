from telethon import TelegramClient
import logging
from config import API_ID, API_HASH

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


client = TelegramClient('test', API_ID, API_HASH)
groups = ['https://t.me/test213121', 'https://t.me/testrsrsr']
async def main():
    for group in groups:
        for i in range(3):
            await client.send_message(group, 'hi')
with client:
    client.loop.run_until_complete(main())

