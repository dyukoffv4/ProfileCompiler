"""Нормализация и преобразование конфигурации."""

from typing import Any


ConfigSource = dict[str, list[dict[str, Any]]]
ConfigNormalized = dict[str, dict[str, list[str]]]


def normalize_endpoint_template(endpoint: str) -> str:
    """Заменить содержимое каждой пары фигурных скобок на единый шаблон {}."""
    ranges: list[tuple[int, int]] = []
    depth = 0
    start: int | None = None

    for index, char in enumerate(endpoint):
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}":
            if depth == 0:
                raise ValueError(f"Invalid endpoint: {endpoint}")
            depth -= 1
            if depth == 0 and start is not None:
                ranges.append((start, index + 1))
                start = None

    if depth != 0:
        raise ValueError(f"Invalid endpoint: {endpoint}")

    offset = 0
    for s_range, e_range in ranges:
        endpoint = endpoint[:s_range - offset] + "{}" + endpoint[e_range - offset:]
        offset += e_range - s_range - 2

    return endpoint


def normalize_config(config: ConfigSource) -> ConfigNormalized:
    """Очистить значения, объединить сервисы и сгруппировать одинаковые endpoint."""
    normalized: ConfigNormalized = {}

    for raw_service, raw_entries in config.items():
        service = raw_service.strip()
        service_entries = normalized.setdefault(service, {})

        for raw_entry in raw_entries:
            method = raw_entry["type"].strip()
            endpoint = normalize_endpoint_template(raw_entry["endpoint"].strip())
            scripts = [script.strip() for script in raw_entry["scripts"]]
            entry_key = f"{method} {endpoint}"

            service_entries.setdefault(entry_key, []).extend(scripts)

    for entries in normalized.values():
        for entry_key, scripts in entries.items():
            entries[entry_key] = list(dict.fromkeys(scripts))

    return normalized
