"""Типы данных конфигурации."""

from typing import Any

ConfigSource = dict[str, list[dict[str, Any]]]
ConfigNormalized = dict[str, dict[str, list[str]]]
