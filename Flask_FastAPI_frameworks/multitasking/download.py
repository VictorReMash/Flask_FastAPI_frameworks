import requests
import time
import aiohttp
import asyncio
from utils import (
    download_file,
    async_download_file,
    print_stop_time,
    print_download_time,
)


def download(url):
    start_time = time.time()
    response = requests.get(url)
    download_file(url, response.content)
    print_download_time(url, time.time() - start_time)


async def download_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_download_file(session, url) for url in urls]
        await asyncio.gather(*tasks)
    print_stop_time(start_time - time.time())
