"""Основной сценарий обработки конфигурации."""

from pathlib import Path

from app.cli.prompts import ask_confirmation
from configuration import restore_source_config
from profile import create_profile_on_config
from storage import save_json

from .checks import run_conflict_checks
from .loading import load_and_normalize_config, load_and_normalize_profile


def _check_path_available(path: Path) -> bool:
    """Проверить, доступно ли место для файла."""
    return path.resolve().exists()


def process(config_path: Path, output_config_path: Path, profile_path: Path, output_profile_path: Path) -> bool:
    """Обработать конфиг и профиль. Сохранить конфиг и профиль."""
    if profile_path is None:
        print("Требуется указать исходный CSV-файл профиля")
        return False

    print("Загрузка конфига")
    normalized_config = load_and_normalize_config(config_path)
    if normalized_config is None:
        return False

    if not run_conflict_checks(normalized_config):
        return False

    if output_config_path is None or not ask_confirmation("Сохранить измененный конфиг?"):
        print("Новый конфиг не будет сохранен.")
    else:
        if _check_path_available(output_config_path):
            print("Данный путь занят. Укажите другой путь через --output-config.")
        else:
            try:
                output_config = restore_source_config(normalized_config)
                save_json(output_config_path, output_config)
                print(f"Результат сохранён: {output_config_path}")
            except (OSError, ValueError) as error:
                print(f"Не удалось сохранить результат в '{output_config_path}': {error}")

    print('Сборка профиля')
    normalized_profile = load_and_normalize_profile(profile_path)
    if normalized_profile is None:
        return False

    if _check_path_available(output_profile_path):
        print("Данный путь занят. Укажите другой путь через --output.")
        return False

    try:
        result_profile = create_profile_on_config(normalized_profile, normalized_config)
        save_json(output_profile_path, result_profile)
        print(f"Результат сохранён: {output_profile_path}")
    except (OSError, ValueError) as error:
        print(f"Не удалось сохранить результат в '{output_profile_path}': {error}")
        return False

    return True
