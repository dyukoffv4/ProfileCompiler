"""Нормализация и загрузка профиля."""

import math

from .models import ProfileNormalized, ProfileSource, ProfileResult
from domain.configuration import ConfigNormalized, normalize_endpoint_template


def normalize_profile(source: ProfileSource) -> ProfileNormalized:
    result = {}
    for i in source:
        _service, _type, _endpoint = i[0].split(' - ')
        _max, _mean, _count = i[1:]
        result.setdefault(_service.strip(), {}).setdefault(f'{_type.strip()} {normalize_endpoint_template(_endpoint)}', 0)
        result[_service.strip()][f'{_type.strip()} {normalize_endpoint_template(_endpoint)}'] += math.ceil(float(_mean))
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
