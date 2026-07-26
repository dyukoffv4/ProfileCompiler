"""Поиск, вывод и разрешение логических конфликтов конфигурации."""

import re
from collections import defaultdict

from normalization import ConfigNormalized


class ScriptConflict:
    def __init__(self, script: str, locations: tuple[str, ...]):
        self.script = script
        self.locations = locations


class EndpointTemplateConflict:
    def __init__(self, service: str, method: str, template: str, concrete_endpoint: str):
        self.service = service
        self.method = method
        self.template = template
        self.concrete_endpoint = concrete_endpoint


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


def compile_endpoint_template(endpoint: str) -> re.Pattern[str]:
    """Преобразовать endpoint с {} в regex для непустых сегментов пути."""
    escaped_parts = (re.escape(part) for part in endpoint.split("{}"))
    pattern = "[^/]+".join(escaped_parts)
    return re.compile(f"^{pattern}$")


def find_endpoint_template_conflicts(config: ConfigNormalized) -> list[EndpointTemplateConflict]:
    """Найти конкретные endpoint, покрываемые шаблоном того же сервиса и метода."""
    conflicts: list[EndpointTemplateConflict] = []

    for service, entries in config.items():
        endpoints_by_method: dict[str, list[str]] = defaultdict(list)

        for entry in entries:
            method, endpoint = entry.split(" ", 1)
            endpoints_by_method[method].append(endpoint)

        for method, endpoints in endpoints_by_method.items():
            templates = [endpoint for endpoint in endpoints if "{}" in endpoint]
            concrete_endpoints = [endpoint for endpoint in endpoints if "{}" not in endpoint]

            for template in templates:
                template_regex = compile_endpoint_template(template)
                for concrete_endpoint in concrete_endpoints:
                    if template_regex.fullmatch(concrete_endpoint):
                        conflicts.append(
                            EndpointTemplateConflict(
                                service=service,
                                method=method,
                                template=template,
                                concrete_endpoint=concrete_endpoint,
                            )
                        )

    return conflicts


def print_endpoint_template_conflicts(conflicts: list[EndpointTemplateConflict]) -> None:
    """Вывести результат проверки пересечений endpoint-шаблонов."""
    if not conflicts:
        print("Проверка шаблонов: пересечений не найдено.")
        return

    print("Проверка шаблонов: найдены пересечения:")
    for conflict in conflicts:
        print(
            f"\tservice={conflict.service}, method={conflict.method}: "
            f"{conflict.template} <-> {conflict.concrete_endpoint}"
        )


def merge_endpoint_template_conflicts(config: ConfigNormalized, conflicts: list[EndpointTemplateConflict]) -> ConfigNormalized:
    """Перенести скрипты конкретных endpoint в шаблоны и удалить конкретные записи."""
    for conflict in conflicts:
        entries = config[conflict.service]
        template_key = f"{conflict.method} {conflict.template}"
        concrete_key = f"{conflict.method} {conflict.concrete_endpoint}"

        if concrete_key not in entries:
            continue

        merged_scripts = entries[template_key] + entries[concrete_key]
        entries[template_key] = list(dict.fromkeys(merged_scripts))
        del entries[concrete_key]

    return config
