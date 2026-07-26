"""Проверка пересечений UC-скриптов."""

from collections import defaultdict

from configuration import ConfigNormalized

from .models import ScriptConflict


def find_script_conflicts(config: ConfigNormalized) -> list[ScriptConflict]:
    """Найти UC-скрипты, присутствующие в двух и более списках."""
    script_locations: dict[str, list[str]] = defaultdict(list)

    for service, entries in config.items():
        for entry, scripts in entries.items():
            for script in dict.fromkeys(scripts):
                script_locations[script].append(f"{service}: {entry}")

    return [
        ScriptConflict(script=script, locations=tuple(locations))
        for script, locations in sorted(script_locations.items())
        if len(locations) >= 2
    ]


def print_script_conflicts(conflicts: list[ScriptConflict]) -> None:
    """Вывести результат проверки пересечений UC-скриптов."""
    if not conflicts:
        print("Проверка скриптов: пересечений не найдено.")
        return

    print("Проверка скриптов: найдены пересечения:")
    for conflict in conflicts:
        print(f"\t{conflict.script}:")
        for location in conflict.locations:
            print(f"\t\t{location}")
