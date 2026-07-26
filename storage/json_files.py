"""Чтение и запись JSON-файлов."""

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """Прочитать JSON-файл и вернуть десериализованный объект."""
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: str | Path, data: Any) -> None:
    """Сериализовать объект и записать его в JSON-файл."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
