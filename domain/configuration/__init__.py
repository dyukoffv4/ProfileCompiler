"""Публичный API работы с конфигурацией."""

from .models import ConfigNormalized, ConfigSource, EndpointConfig, NormalizedConfig, ScriptsConfig
from .normalization import normalize_config, normalize_endpoint_template

__all__ = [
    "ConfigNormalized",
    "ConfigSource",
    "EndpointConfig",
    "NormalizedConfig",
    "ScriptsConfig",
    "normalize_config",
    "normalize_endpoint_template"
]
