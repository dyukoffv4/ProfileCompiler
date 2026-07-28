"""Загрузка, проверка и нормализация входного конфига."""

import json
import csv
from pathlib import Path

from domain.configuration import ConfigNormalized, normalize_config, validate_config_structure
from domain.profile import ProfileNormalized, normalize_profile
from infrastructure.storage import load_json, load_csv


def load_and_normalize_config(source_path: Path) -> ConfigNormalized | None:
    """Загрузить JSON, проверить структуру и привести данные к единому виду."""
    try:
        source_config = load_json(source_path)
    except OSError as error:
        print(f"Не удалось прочитать конфиг '{source_path}': {error}")
        return None
    except json.JSONDecodeError as error:
        print(f"Некорректный JSON в '{source_path}': {error}")
        return None

    if not validate_config_structure(source_config):
        return None

    try:
        return normalize_config(source_config)
    except ValueError as error:
        print(error)
        return None


def load_and_normalize_profile(source_path: Path) -> ProfileNormalized | None:
    """Загрузить CSV и привести данные к единому виду."""
    try:
        source_profile = load_csv(source_path)
    except OSError as error:
        print(f"Не удалось прочитать профиль '{source_path}': {error}")
        return None
    except csv.Error as error:
        print(f"Некорректный CSV в '{source_path}': {error}")
        return None

    try:
        return normalize_profile(source_profile)
    except ValueError as error:
        print(error)
        return None
