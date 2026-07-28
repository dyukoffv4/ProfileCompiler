"""Проверка пересечений UC-скриптов."""

from collections import defaultdict

from domain.configuration import ConfigNormalized
from .models import ScriptConflict


def find_script_conflicts(config: ConfigNormalized) -> list[ScriptConflict]:
    locations = defaultdict(list)
    for service, entries in config.services.items():
        for entry, scripts in entries.items():
            for script in dict.fromkeys(scripts):
                locations[script].append(f"{service}: {entry}")
    return [ScriptConflict(s, tuple(v)) for s, v in sorted(locations.items()) if len(v) >= 2]


def find_static_script_conflicts(config: ConfigNormalized) -> list[str]:
    static = set(config.statics)
    main = {s for entries in config.services.values() for scripts in entries.values() for s in scripts}
    return sorted(static & main)


def print_script_conflicts(conflicts):
    if not conflicts:
        print("Проверка скриптов: пересечений не найдено.")
        return
    print("Проверка скриптов: найдены пересечения:")
    for conflict in conflicts:
        if isinstance(conflict, str):
            print(f"\t{conflict}")
        else:
            print(f"\t{conflict.script}:")
            for location in conflict.locations:
                print(f"\t\t{location}")
