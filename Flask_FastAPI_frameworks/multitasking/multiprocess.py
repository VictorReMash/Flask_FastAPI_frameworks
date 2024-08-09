from multiprocessing import Process
import time
from download import download
from parser import parsing_cmd
from utils import print_stop_time


def multiprocessing_download(urls):
    start_time = time.time()
    processes = [Process(target=download, args=(url,)) for url in urls]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print_stop_time(time.time() - start_time)


if __name__ == "__main__":
    args = parsing_cmd()
    urls = args.urls
    multiprocessing_download(urls)
