"""Проверки пересечений скриптов конфигурации."""

from collections import defaultdict

from domain.configuration import ConfigNormalized

from .models import ScriptConflict


def find_static_script_conflicts(config: ConfigNormalized) -> list[str]:
    """Найти пересечения внешних statics со scripts/statics внутри сервисов."""
    internal = set()
    for entries in config.services.values():
        for entry in entries.values():
            internal.update(entry.scripts)
            internal.update(entry.statics)
    return sorted(set(config.statics) & internal)


def find_script_conflicts(config: ConfigNormalized) -> list[ScriptConflict]:
    """Найти скрипты, используемые более чем в одном endpoint.

    Такие пересечения допустимы: при сборке профиля интенсивности скрипта
    суммируются. Фатальные пересечения внутри одного endpoint и с внешними
    statics отсекаются на этапе нормализации.
    """
    locations: dict[str, list[str]] = defaultdict(list)

    for service, entries in config.services.items():
        for endpoint, entry in entries.items():
            for script in dict.fromkeys(entry.scripts):
                locations[script].append(f"{service}: {endpoint} [scripts]")
            for script in entry.statics:
                locations[script].append(f"{service}: {endpoint} [statics]")

    return [
        ScriptConflict(script, tuple(script_locations))
        for script, script_locations in sorted(locations.items())
        if len(script_locations) > 1
    ]


def print_script_conflicts(conflicts: list[ScriptConflict]) -> None:
    """Предупредить о скриптах, интенсивности которых будут суммированы."""
    if not conflicts:
        print("Проверка скриптов: совпадений между endpoint не найдено.")
        return

    print("Проверка скриптов: найдены совпадения между endpoint.")
    print("Интенсивности этих скриптов в итоговом профиле будут суммированы:")
    for conflict in conflicts:
        print(f"\t{conflict.script}:")
        for location in conflict.locations:
            print(f"\t\t{location}")
