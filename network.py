import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_server_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch page: {response.status}")
            html_content = await response.text()

            soup = BeautifulSoup(html_content, 'html.parser')
            server_row = soup.find("div", class_="card-body")

            player_count_span_green = server_row.find("span", class_="c-green")
            server_status = server_row.find("span", class_="c-red")

            if player_count_span_green:
                string = str(player_count_span_green.text.strip())
                string = string.replace("Online ", "")
                return f"🎮 Онлайн {string}"
            elif server_status:
                return f"❌ {server_status.text.strip()} ❌"
            else:
                raise Exception("Player count not found")

async def main():
    online = await fetch_server_data("https://wargm.ru/server/73928")
    print(online)


if __name__ == "__main__": 
    asyncio.run(main())