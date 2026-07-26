"""Модели найденных конфликтов."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScriptConflict:
    """Скрипт, присутствующий в нескольких местах конфигурации."""

    script: str
    locations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EndpointTemplateConflict:
    """Пересечение шаблонного и конкретного endpoint."""

    service: str
    method: str
    template: str
    concrete_endpoint: str
