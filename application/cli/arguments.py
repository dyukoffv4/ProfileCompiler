"""Настройка аргументов командной строки."""

import argparse
from pathlib import Path

DEFAULT_SOURCE_PATH = Path("configs/config.json")
DEFAULT_OUTPUT_PATH = Path("results/profile.json")


def build_argument_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description=(
            "Обработать конфиг и профиль. Сохранить конфиг и профиль. "
            "Относительные пути вычисляются от текущей рабочей директории."
        )
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
        help=f"путь к исходному JSON-конфигу (по умолчанию: {DEFAULT_SOURCE_PATH})",
    )
    parser.add_argument(
        "--config-output",
        type=Path,
        default=None,
        help=f"путь для измененного JSON-конфига",
    )
    parser.add_argument(
        "-p",
        "--profile",
        type=Path,
        default=None,
        help=f"путь к исходному CSV-профилю",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"путь для результата (по умолчанию: {DEFAULT_OUTPUT_PATH})",
    )
    return parser
