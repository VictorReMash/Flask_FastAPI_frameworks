import argparse


def parsing_cmd():
    parser = argparse.ArgumentParser(
        description="Скачивание изображений с указанных URL."
    )
    parser.add_argument(
        "urls",
        metavar="URL",
        type=str,
        nargs="+",
        help="Список URL изображений для скачивания",
    )
    return parser.parse_args()
