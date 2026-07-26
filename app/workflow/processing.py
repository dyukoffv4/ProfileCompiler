"""Основной сценарий обработки конфигурации."""

from pathlib import Path

from storage import save_json

from .checks import run_conflict_checks
from .loading import load_and_normalize_config


def process_config(source_path: Path, output_path: Path) -> bool:
    """Обработать конфиг и сохранить результат в указанный файл."""
    normalized_config = load_and_normalize_config(source_path)
    if normalized_config is None:
        return False

    if not run_conflict_checks(normalized_config):
        return False

    try:
        save_json(output_path, normalized_config)
    except OSError as error:
        print(f"Не удалось сохранить результат в '{output_path}': {error}")
        return False

    print(f"Результат сохранён: {output_path}")
    return True
