"""Основной сценарий обработки конфигурации."""

from pathlib import Path

from application.cli.prompts import ask_confirmation
from domain.configuration import restore_source_config
from domain.profile import create_profile_on_config
from infrastructure.storage import save_json

from .checks import run_conflict_checks
from .loading import load_and_normalize_config, load_and_normalize_profile


def process(config_path: Path, output_config_path: Path, profile_path: Path, output_profile_path: Path) -> bool:
    """Обработать конфиг и профиль. Сохранить конфиг и профиль."""

    print("Загрузка конфига")
    if config_path is None:
        print("Требуется указать JSON-файл конфига")
        return False

    normalized_config = load_and_normalize_config(config_path)
    if normalized_config is None:
        return False

    if not run_conflict_checks(normalized_config):
        return False

    if output_config_path is None or not ask_confirmation("Сохранить измененный конфиг?"):
        print("Новый конфиг не будет сохранен. Чтобы сохранить его укажите путь через --output-config.")
    else:
        if output_config_path.exists():
            print("Данный путь занят. Укажите другой путь через --output-config.")
        else:
            try:
                output_config = restore_source_config(normalized_config)
                save_json(output_config_path, output_config)
                print(f"Результат сохранён: {output_config_path}")
            except (OSError, ValueError) as error:
                print(f"Не удалось сохранить результат в '{output_config_path}': {error}")

    print('Сборка профиля')
    if profile_path is None:
        print("Требуется указать исходный CSV-файл данных выгрузки")
        return False

    if output_profile_path is None:
        print("Требуется указать путь сохранения профиля")
        return False

    normalized_profile = load_and_normalize_profile(profile_path)
    if normalized_profile is None:
        return False

    if output_profile_path.exists():
        if not ask_confirmation(f"Файл '{output_profile_path}' уже существует. Перезаписать его?"):
            print("Файл профиля не будет перезаписан.")
            return False

    try:
        result_profile = create_profile_on_config(normalized_profile, normalized_config)
        save_json(output_profile_path, result_profile)
        print(f"Результат сохранён: {output_profile_path}")
    except (OSError, ValueError) as error:
        print(f"Не удалось сохранить результат в '{output_profile_path}': {error}")
        return False

    return True
