"""Чтение и запись текстовых файлов."""

from pathlib import Path


def load_text(path: str | Path) -> str:
    """Прочитать текстовый файл и вернуть его содержимое."""
    return Path(path).read_text(encoding="utf-8")


def save_text(path: str | Path, data: str) -> None:
    """Записать строку в текстовый файл."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(data, encoding="utf-8")
