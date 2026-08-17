"""Нормализация и сборка профиля нагрузки."""

import math

from domain.configuration import ConfigNormalized, EndpointConfig, normalize_endpoint_template

from .models import ProfileNormalized, ProfileResult, ProfileSource


def normalize_profile(source: ProfileSource) -> ProfileNormalized:
    result = {}
    for row in source:
        service, method, endpoint = [i.strip() for i in row[0].split(" - ", maxsplit=2)]
        maximum, mean = row[1:3]
        normalized_entry = f"{method} {normalize_endpoint_template(endpoint)}"
        service_entries = result.setdefault(service, {})
        service_entries.setdefault(normalized_entry, 0)
        service_entries[normalized_entry] += math.ceil(float(mean))
    return result


def _add_endpoint_scripts(result: ProfileResult, source_intensity: int, config: EndpointConfig) -> None:
    scripts_intensity = source_intensity
    if config.statics_diff:
        scripts_intensity -= sum(config.statics.values())

    if isinstance(config.scripts, list):
        if config.scripts:
            per_script = math.ceil(scripts_intensity / len(config.scripts))
            for script in config.scripts:
                result[script] = result.get(script, 0) + per_script
    else:
        for script, coefficient in config.scripts.items():
            result[script] = result.get(script, 0) + math.ceil(scripts_intensity * coefficient)


def _add_endpoint_statics(result: ProfileResult, config: EndpointConfig) -> None:
    for script, intensity in config.statics.items():
        result[script] = result.get(script, 0) + intensity


def create_profile_on_config(profile: ProfileNormalized, config: ConfigNormalized) -> ProfileResult:
    result: ProfileResult = {}

    for service, entries in config.services.items():
        for entry, entry_config in entries.items():
            _add_endpoint_statics(result, entry_config)

            source_intensity = profile.get(service, {}).get(entry)
            if source_intensity is None:
                continue
            _add_endpoint_scripts(result, source_intensity, entry_config)

    result.update(config.statics)
    return result
