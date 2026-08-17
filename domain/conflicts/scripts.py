"""Проверки пересечений скриптов конфигурации."""

from domain.configuration import ConfigNormalized


def find_static_script_conflicts(config: ConfigNormalized) -> list[str]:
    """Найти пересечения внешних statics со scripts/statics внутри сервисов."""
    internal = set()
    for entries in config.services.values():
        for entry in entries.values():
            internal.update(entry.scripts)
            internal.update(entry.statics)
    return sorted(set(config.statics) & internal)
