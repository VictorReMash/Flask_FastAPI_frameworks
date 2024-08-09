from multiprocessing import Process
import time
from download import download_sync
from parser import parsing_cmd


def multiprocessing_download(urls):
    start_time = time.time()
    processes = [Process(target=download_sync, args=(url,)) for url in urls]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print(f"Общее время выполнения (процессы): {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    args = parsing_cmd()
    urls = args.urls
    multiprocessing_download(urls)
