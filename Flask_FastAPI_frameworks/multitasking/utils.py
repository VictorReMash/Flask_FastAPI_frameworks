import os
import time
import requests
import aiohttp


def download_file(url, content):
    filename = os.path.basename(url)
    with open(filename, "wb") as f:
        f.write(content)


async def async_download_file(session, url):
    async with session.get(url) as response:
        content = await response.read()
        download_file(url, content)
