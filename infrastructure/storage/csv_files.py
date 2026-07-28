"""Чтение и запись CSV-файлов."""

import csv
from pathlib import Path


def load_csv(path: str | Path, *, delimiter: str = ",") -> list[list[str]]:
    """Прочитать CSV-файл как список строк."""
    with Path(path).open("r", encoding="utf-8", newline="") as file:
        return list(csv.reader(file, delimiter=delimiter))


def save_csv(path: str | Path, rows: list[list[str]], *, delimiter: str = ",") -> None:
    """Записать строки в CSV-файл."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as file:
        csv.writer(file, delimiter=delimiter).writerows(rows)
