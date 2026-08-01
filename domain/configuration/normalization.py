"""Нормализация и преобразование конфигурации."""

from .models import ConfigSource, ConfigNormalized, NormalizedConfig


def normalize_endpoint_template(endpoint: str) -> str:
    ranges = []
    depth = 0
    start = None
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
    if depth:
        raise ValueError(f"Invalid endpoint: {endpoint}")
    offset = 0
    for a, b in ranges:
        endpoint = endpoint[:a-offset] + "{}" + endpoint[b-offset:]
        offset += b-a-2
    return endpoint


def normalize_config(config: ConfigSource) -> ConfigNormalized:
    main = config.get("main", config)
    normalized = {}

    for raw_service, raw_entries in main.items():
        service = raw_service.strip()
        entries = normalized.setdefault(service, {})

        for raw_entry in raw_entries:
            method = raw_entry["type"].strip()
            endpoint = normalize_endpoint_template(raw_entry["endpoint"].strip())
            key = f"{method} {endpoint}"
            entries.setdefault(key, []).extend(x.strip() for x in raw_entry["scripts"])

    for entries in normalized.values():
        for key, scripts in entries.items():
            entries[key] = list(dict.fromkeys(scripts))

    statics = {k.strip(): v for k, v in config.get("statics", {}).items()}
    if len(statics) != len(config.get("statics", {})):
        raise ValueError("Найдены одинаковые статичные скрипты после нормализации")

    return NormalizedConfig(normalized, statics)


def restore_source_config(config: ConfigNormalized) -> ConfigSource:
    result = {"main": {}, "statics": config.statics}

    for service, entries in config.services.items():
        for key, scripts in entries.items():
            if result["main"].get(service) is None:
                result["main"][service] = []
            method, endpoint = key.split(" ",1)
            result["main"][service].append({"type": method, "endpoint": endpoint, "scripts": scripts})

    return result
