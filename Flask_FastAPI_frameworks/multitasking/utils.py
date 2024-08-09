import os
import time


def print_start_time(time):
    print(f"Запуск метода скачивания: {time}")


def print_download_time(url, time):
    print(f"Загружено {url} за {time:.2f} секунд")


def print_stop_time(time):
    print(f"Общее время выполнения (процессы): {time:.2f} секунд")


def download_file(url, content):
    filename = os.path.basename(url)
    with open(filename, "wb") as f:
        f.write(content)


async def async_download_file(session, url):
    async with session.get(url) as response:
        start_time = time.time()
        content = await response.read()
        download_file(url, content)
        print_download_time(url, time.time() - start_time)
