"""Проверка и объединение конфликтующих endpoint-шаблонов."""

import re
from collections import defaultdict

from domain.configuration import ConfigNormalized

from .models import EndpointTemplateConflict


def compile_endpoint_template(endpoint: str) -> re.Pattern[str]:
    """Преобразовать endpoint с ``{}`` в regex непустых сегментов пути."""
    escaped_parts = (re.escape(part) for part in endpoint.split("{}"))
    pattern = "[^/]+".join(escaped_parts)
    return re.compile(f"^{pattern}$")


def find_endpoint_template_conflicts(config: ConfigNormalized) -> list[EndpointTemplateConflict]:
    """Найти конкретные endpoint, покрываемые шаблоном сервиса и метода."""
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
                        conflicts.append(EndpointTemplateConflict(service, method, template, concrete_endpoint))

    return conflicts


def print_endpoint_template_conflicts(conflicts: list[EndpointTemplateConflict]) -> None:
    """Вывести результат проверки пересечений endpoint-шаблонов."""
    if not conflicts:
        print("Проверка шаблонов: пересечений не найдено.")
        return

    print("Проверка шаблонов: найдены пересечения:")
    for conflict in conflicts:
        print(f"\tservice={conflict.service}, method={conflict.method}: {conflict.template} <-> {conflict.concrete_endpoint}")
