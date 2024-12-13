import discord
from discord.ext import tasks
import asyncio
from network import fetch_server_data
import bot_tokens
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# Создаем класс для управления отдельным ботом
class AsyncBot:
    def __init__(self, bot_tokens, server_url, description):
        self.bot_tokens = bot_tokens
        self.server_url = server_url
        self.description = description
        self.intents = discord.Intents.default()
        self.bot = discord.Client(intents=self.intents)
        self.description_counter = 0

        @self.bot.event
        async def on_ready():
            logger.info(f"Logged in as {self.bot.user}")
            if self.description == "":
                self.update_bot_description.start()
            else:
                await self.bot.change_presence(activity=discord.Game(name=self.description))

    @tasks.loop(seconds=60)
    async def update_bot_description(self):
        try:
            self.description_counter += 1
            new_description = await fetch_server_data(self.server_url)
            await self.bot.change_presence(activity=discord.Game(name=new_description))
        except Exception as e:
            logger.error(f"Error updating description for bot {self.bot.user}: {e}")
            await asyncio.sleep(10)

    async def start_bot(self):
        await self.bot.start(self.bot_tokens)

# Асинхронный запуск нескольких ботов
async def main():
    bots = [
        AsyncBot(bot_tokens.bot_1, "https://wargm.ru/server/73093", "Ведутся Тех. Работы"),
        AsyncBot(bot_tokens.bot_2, "https://wargm.ru/server/73928", ""),
        # Добавьте дополнительные боты по необходимости
    ]

    await asyncio.gather(*(bot.start_bot() for bot in bots))

if __name__ == "__main__":
    asyncio.run(main())


# import discord
# from discord.ext import tasks
# import asyncio
# from network import fetch_server_data
# from aiohttp_socks import ProxyConnector
# import aiohttp
# import bot_tokens
# from proxy import proxy_host, proxy_port, proxy_username, proxy_password

# # Создаем класс для управления отдельным ботом
# class AsyncBot:
#     def __init__(self, bot_token, server_url, proxy_url=None):
#         self.bot_token = bot_token
#         self.server_url = server_url
#         self.proxy_url = proxy_url
#         self.intents = discord.Intents.default()
#         self.bot = discord.Client(intents=self.intents)

#         @self.bot.event
#         async def on_ready():
#             print(f"Logged in as {self.bot.user}")
#             self.update_bot_description.start()

#         self.update_bot_description = tasks.loop(seconds=60)(self.update_bot_description)
    
#     async def update_bot_description(self):
#         try:
#             new_description = await fetch_server_data(self.server_url)
#             await self.bot.change_presence(activity=discord.Game(name=new_description))
#         except Exception as e:
#             print(f"Error updating description for bot {self.bot.user}: {e}")
#             await asyncio.sleep(10)
    
#     async def start_bot(self):
#         try:
#             if self.proxy_url:
#                 connector = ProxyConnector.from_url(self.proxy_url)
#                 session = aiohttp.ClientSession(connector=connector)
#                 self.bot.http.session = session
#                 await self.bot.start(self.bot_token)
#             else:
#                 await self.bot.start(self.bot_token)
#         except Exception as e:
#             print(f"Ошибка при запуске бота: {e}")

# # Асинхронный запуск нескольких ботов
# async def main():



#     proxy_url = f"socks5://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

#     bots = [
#         AsyncBot(
#             bot_tokens.bot_1,
#             "https://wargm.ru/server/73093",
#             proxy_url,
#         ),
#         AsyncBot(
#             bot_tokens.bot_2,
#             "https://wargm.ru/server/73928",
#             proxy_url,
#         ),
#         # Добавьте дополнительных ботов по необходимости
#     ]

#     await asyncio.gather(*(bot.start_bot() for bot in bots))

# if __name__ == "__main__":
#     asyncio.run(main())