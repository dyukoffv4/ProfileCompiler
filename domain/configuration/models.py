"""Типы данных конфигурации."""

from dataclasses import dataclass
from typing import Any

ConfigSource = dict[str, Any]
ScriptsConfig = list[str] | dict[str, float]


@dataclass
class EndpointConfig:
    """Нормализованные настройки одного эндпоинта."""

    scripts: ScriptsConfig
    statics: dict[str, int]
    statics_diff: bool = True


@dataclass
class NormalizedConfig:
    """Нормализованный конфиг с сервисами и внешними статичными данными."""

    services: dict[str, dict[str, EndpointConfig]]
    statics: dict[str, int]


ConfigNormalized = NormalizedConfig
