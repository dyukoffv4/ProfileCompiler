"""Основной сценарий обработки задач."""

from pathlib import Path

from application.cli.prompts import ask_confirmation
from domain.configuration import restore_source_config
from domain.profile import create_profile_on_config
from infrastructure.storage import save_json

from .checks import run_conflict_checks
from .coverage import run_coverage_analysis
from .loading import load_and_normalize_config, load_and_normalize_profile


def _save_process(save_path: Path, save_data):
    if save_path is None:
        return False

    if save_path.exists() and not ask_confirmation(f"Файл '{save_path}' уже существует. Перезаписать его?"):
        print(f"Файл '{save_path}' не будет перезаписан.")
        return False

    try:
        save_json(save_path, save_data)
        print(f"Результат сохранён: {save_path}")
    except (OSError, ValueError) as error:
        print(f"Не удалось сохранить результат в '{save_path}': {error}")
        return False

    return True


def process(config_path: Path, output_config_path: Path, profile_path: Path, output_profile_path: Path) -> bool:
    # Обработать конфиг

    print("\n--- Загрузка конфига ---\n")
    if config_path is None:
        print("Требуется указать JSON-файл конфига")
        return False

    normalized_config = load_and_normalize_config(config_path)
    if normalized_config is None:
        return False

    # Проверить конфиг

    if not run_conflict_checks(normalized_config):
        return False
    print()

    # Сохранить конфиг

    if output_config_path is None:
        print("Новый конфиг не будет сохранен. Чтобы сохранить его укажите путь через --output-config.")
    else:
        _save_process(output_config_path, restore_source_config(normalized_config))

    # Обработать профиль

    print('\n--- Сборка профиля ---\n')
    if profile_path is None:
        print("Требуется указать исходный CSV-файл данных выгрузки")
        return False

    normalized_profile = load_and_normalize_profile(profile_path)
    if normalized_profile is None:
        return False

    # Проверить профиль

    if not run_coverage_analysis(normalized_profile, normalized_config):
        return False
    print()

    # Сохранить профиль

    if output_profile_path is None:
        print("Собранный профиль не будет сохранен. Чтобы сохранить его укажите путь через --output.")
    else:
        _save_process(output_profile_path, create_profile_on_config(normalized_profile, normalized_config))

    return True
