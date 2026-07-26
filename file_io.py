"""Функции чтения и записи текстовых файлов."""

from pathlib import Path


def load_text(path: str | Path) -> str:
    """Прочитать текстовый файл и вернуть его содержимое."""
    return Path(path).read_text(encoding="utf-8")


def save_text(path: str | Path, data: str) -> None:
    """Записать строку в текстовый файл."""
    Path(path).write_text(data, encoding="utf-8")
