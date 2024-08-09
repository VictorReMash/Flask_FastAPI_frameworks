import argparse
import asyncio
import time
from download import download_async, download
from multithread import multithreaded_download
from multiprocess import multiprocessing_download
from utils import print_start_time, print_stop_time


def main():
    parser = argparse.ArgumentParser(description="Скачивание изображений.")
    parser.add_argument(
        "urls",
        metavar="URL",
        type=str,
        nargs="+",
        help="Список URL изображений для скачивания",
    )
    parser.add_argument(
        "--method",
        choices=["sync", "threads", "processes", "async"],
        default="sync",
        help="Метод скачивания (sync, threads, processes, async)",
    )
    args = parser.parse_args()

    if args.method == "sync":
        print_start_time(args.method)
        start_time = time.time()
        for url in args.urls:
            download(url)
        print_stop_time(time)
    elif args.method == "threads":
        print_start_time(args.method)
        multithreaded_download(args.urls)
    elif args.method == "processes":
        print_start_time(args.method)
        multiprocessing_download(args.urls)
    elif args.method == "async":
        print_start_time(args.method)
        asyncio.run(download_async(args.urls))


if __name__ == "__main__":
    main()
