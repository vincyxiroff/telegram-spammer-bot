from telethon import TelegramClient
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)



class Send:
    def __init__(self, api_id, api_hash) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('test', api_id, api_hash)

    async def sendall(self, groups, message_text):
        self.errors = {}

        for group in groups:
            try:
                await self.client.send_message(group, message_text)
            except Exception as e:
                self.errors['group'] = e
        
        


    async def start(self, groups, message_text):
        with self.client:
            self.client.loop.run_until_complete(
                                        self.sendall(groups, message_text))


