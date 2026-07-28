"""Типы данных конфигурации."""

from dataclasses import dataclass
from typing import Any

ConfigSource = dict[str, Any]


@dataclass
class NormalizedConfig:
    """Нормализованный конфиг с основными и статичными данными."""

    services: dict[str, dict[str, list[str]]]
    statics: dict[str, int]


ConfigNormalized = NormalizedConfig
