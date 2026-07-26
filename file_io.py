"""Функции чтения и записи текстовых файлов."""

from pathlib import Path
from typing import Any
import json
import csv


def load_text(path: str | Path) -> str:
    """Прочитать текстовый файл и вернуть его содержимое."""
    return Path(path).read_text(encoding="utf-8")


def load_json(path: str | Path) -> Any:
    """Прочитать JSON файл и вернуть его в виде объекта."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_csv(path: str | Path, *, delimiter: str = ",") -> list[list[str]]:
    """Прочитать CSV-файл как список."""
    with Path(path).open("r", encoding="utf-8", newline="") as file:
        return [i for i in csv.reader(file, delimiter=delimiter)]


def save_text(path: str | Path, data: str) -> None:
    """Записать строку в текстовый файл."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def save_json(path: str | Path, data: Any) -> None:
    """Записать объект в текстовый файл в формате JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4), encoding="utf-8")


def save_csv(path: str | Path, rows: list[list[str]], *, delimiter: str = ",") -> None:
    """Записать список в CSV-файл."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(rows)
