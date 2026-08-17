"""Нормализация и преобразование конфигурации."""

from .models import ConfigSource, ConfigNormalized, EndpointConfig, NormalizedConfig, ScriptsConfig


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


def _normalize_scripts(raw_scripts) -> ScriptsConfig:
    if isinstance(raw_scripts, list):
        scripts = [script.strip() for script in raw_scripts]
        if len(scripts) != len(set(scripts)):
            raise ValueError("Найдены повторяющиеся scripts внутри одного эндпоинта")
        return scripts

    if isinstance(raw_scripts, dict):
        scripts = {script.strip(): coefficient for script, coefficient in raw_scripts.items()}
        if len(scripts) != len(raw_scripts):
            raise ValueError("Найдены одинаковые scripts после нормализации внутри одного эндпоинта")
        return scripts

    raise ValueError("Поле 'scripts' эндпоинта должно быть списком или словарём")


def _normalize_statics(raw_statics) -> dict[str, int]:
    if raw_statics is None:
        return {}
    if not isinstance(raw_statics, dict):
        raise ValueError("Поле 'statics' эндпоинта должно быть словарём")

    statics = {script.strip(): intensity for script, intensity in raw_statics.items()}
    if len(statics) != len(raw_statics):
        raise ValueError("Найдены одинаковые statics после нормализации внутри одного эндпоинта")
    return statics


def normalize_config(config: ConfigSource) -> ConfigNormalized:
    """Нормализовать конфиг фиксированной структуры ``main`` + ``statics``."""
    try:
        main = config["main"]
        raw_global_statics = config["statics"]
    except (KeyError, TypeError) as error:
        raise ValueError("Конфиг должен содержать объекты 'main' и 'statics'") from error

    normalized: dict[str, dict[str, EndpointConfig]] = {}

    for raw_service, raw_entries in main.items():
        service = raw_service.strip()
        entries = normalized.setdefault(service, {})

        for raw_entry in raw_entries:
            try:
                method = raw_entry["type"].strip()
                endpoint = normalize_endpoint_template(raw_entry["endpoint"].strip())
                scripts = _normalize_scripts(raw_entry["scripts"])
            except (KeyError, TypeError, AttributeError) as error:
                raise ValueError("Каждый эндпоинт должен содержать 'endpoint', 'type' и 'scripts'") from error

            statics = _normalize_statics(raw_entry.get("statics"))
            statics_diff = raw_entry.get("statics_diff", True)
            if not isinstance(statics_diff, bool):
                raise ValueError("Поле 'statics_diff' должно быть boolean")

            script_names = set(scripts)
            intersections = sorted(script_names & set(statics))
            if intersections:
                location = f"{service}: {method} {endpoint}"
                names = ", ".join(intersections)
                raise ValueError(
                    f"Пересечение scripts и statics внутри эндпоинта '{location}': {names}"
                )

            key = f"{method} {endpoint}"
            entries[key] = EndpointConfig(
                scripts=scripts,
                statics=statics,
                statics_diff=statics_diff,
            )

    if not isinstance(raw_global_statics, dict):
        raise ValueError("Внешнее поле 'statics' должно быть словарём")

    global_statics = {script.strip(): intensity for script, intensity in raw_global_statics.items()}
    if len(global_statics) != len(raw_global_statics):
        raise ValueError("Найдены одинаковые внешние statics после нормализации")

    internal_scripts = set()
    for entries in normalized.values():
        for entry in entries.values():
            internal_scripts.update(entry.scripts)
            internal_scripts.update(entry.statics)

    intersections = sorted(set(global_statics) & internal_scripts)
    if intersections:
        raise ValueError(
            "Внешние statics пересекаются со скриптами внутри сервисов: "
            + ", ".join(intersections)
        )

    return NormalizedConfig(normalized, global_statics)


def restore_source_config(config: ConfigNormalized) -> ConfigSource:
    result = {"main": {}, "statics": config.statics}

    for service, entries in config.services.items():
        result["main"][service] = []
        for key, entry_config in entries.items():
            method, endpoint = key.split(" ", 1)
            source_entry = {
                "endpoint": endpoint,
                "type": method,
                "scripts": entry_config.scripts,
            }
            if entry_config.statics:
                source_entry["statics"] = entry_config.statics
            if entry_config.statics_diff is not True:
                source_entry["statics_diff"] = entry_config.statics_diff
            result["main"][service].append(source_entry)

    return result
