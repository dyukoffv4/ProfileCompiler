"""Основной сценарий обработки конфигурации."""

from pathlib import Path

from app.cli.prompts import ask_to_save
from configuration import restore_source_config
from storage import save_json

from .checks import run_conflict_checks
from .loading import load_and_normalize_config


def _paths_point_to_same_file(source_path: Path, output_path: Path) -> bool:
    """Проверить, указывают ли входной и выходной пути на один файл."""
    return source_path.resolve() == output_path.resolve()


def process_config(source_path: Path, output_path: Path) -> bool:
    """Обработать конфиг и при подтверждении сохранить новый файл."""
    normalized_config = load_and_normalize_config(source_path)
    if normalized_config is None:
        return False

    if not run_conflict_checks(normalized_config):
        return False

    if not ask_to_save():
        print("Результат не сохранён.")
        return True

    if _paths_point_to_same_file(source_path, output_path):
        print("Исходный конфиг не будет перезаписан. Укажите другой путь через --output.")
        return False

    try:
        output_config = restore_source_config(normalized_config)
        save_json(output_path, output_config)
    except (OSError, ValueError) as error:
        print(f"Не удалось сохранить результат в '{output_path}': {error}")
        return False

    print(f"Результат сохранён: {output_path}")
    return True
