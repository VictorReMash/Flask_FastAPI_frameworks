import requests
import time
import aiohttp
import asyncio
from utils import download_file, async_download_file


def download_sync(url):
    start_time = time.time()
    response = requests.get(url)
    download_file(url, response.content)
    print(f"Загружено {url} за {time.time() - start_time:.2f} секунд")


async def download_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_download_file(session, url) for url in urls]
        await asyncio.gather(*tasks)
    print(f"Общее время выполнения (асинхронно): {time.time() - start_time:.2f} секунд")
