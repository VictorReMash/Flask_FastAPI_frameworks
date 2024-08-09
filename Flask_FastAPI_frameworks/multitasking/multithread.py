import threading
import time
from download import download_sync
from parser import parsing_cmd


def multithreaded_download(urls):
    start_time = time.time()
    threads = [threading.Thread(target=download_sync, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Общее время выполнения (потоки): {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    args = parsing_cmd()
    urls = args.urls
    multithreaded_download(urls)
