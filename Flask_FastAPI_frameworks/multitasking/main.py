import argparse
import asyncio
from download import download_async, download_sync
from multithread import multithreaded_download
from multiprocess import multiprocessing_download


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
        for url in args.urls:
            download_sync(url)
    elif args.method == "threads":
        multithreaded_download(args.urls)
    elif args.method == "processes":
        multiprocessing_download(args.urls)
    elif args.method == "async":
        asyncio.run(download_async(args.urls))


if __name__ == "__main__":
    main()
