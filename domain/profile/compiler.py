"""Нормализация и сборка профиля нагрузки."""

import math

from domain.configuration import ConfigNormalized, normalize_endpoint_template

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


def create_profile_on_config(profile: ProfileNormalized, config: ConfigNormalized) -> ProfileResult:
    result = {}
    for service, entries in config.services.items():
        for entry, scripts in entries.items():
            for script in scripts:
                result.setdefault(script, 0)
                if profile.get(service, {}).get(entry) is not None:
                    result[script] += math.ceil(profile[service][entry] / len(scripts))
    result.update(config.statics)
    return result
