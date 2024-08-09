import threading
import time
from download import download
from parser import parsing_cmd
from utils import print_stop_time


def multithreaded_download(urls):
    start_time = time.time()
    threads = [threading.Thread(target=download, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print_stop_time(time.time() - start_time)


if __name__ == "__main__":
    args = parsing_cmd()
    urls = args.urls
    multithreaded_download(urls)
