"""Нормализация и загрузка профиля."""

import math

from .models import ProfileNormalized, ProfileSource, ProfileResult
from configuration import normalize_endpoint_template, ConfigNormalized


def normalize_profile(source: ProfileSource) -> ProfileNormalized:
    """Нормализация исходного профиля к удобному виду"""
    result: ProfileNormalized = {}

    for i in source:
        _service, _type, _endpoint = i[0].split(' - ')
        _max, _mean, _count = i[1:]

        if result.get(s_service := _service.strip()) is None:
            result[s_service.strip()] = {}

        if result[s_service].get(entry := f'{_type.strip()} {normalize_endpoint_template(_endpoint)}') is None:
            result[s_service][entry] = 0

        result[s_service][entry] += math.ceil(float(_mean))

    return result


def create_profile_on_config(profile: ProfileNormalized, config: ConfigNormalized) -> ProfileResult:
    """Получение профиля для работы в сценарии НТ"""
    result: ProfileResult = {}

    for service in config:
        for entry in config[service]:
            for script in config[service][entry]:
                if result.get(script) is None:
                    result[script] = 0
                if profile[service].get(entry) is not None:
                    result[script] += math.ceil(profile[service][entry] / len(config[service][entry]))

    return result
