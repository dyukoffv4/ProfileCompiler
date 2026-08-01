"""Расчёт покрытия интенсивности конфигурацией."""

from domain.configuration import ConfigNormalized
from domain.profile import ProfileNormalized

from .models import CoverageReport, ServiceCoverage


def calculate_coverage(profile: ProfileNormalized, config: ConfigNormalized) -> CoverageReport:
    """Рассчитать покрытие интенсивности и найти непокрытые эндпоинты."""
    report: CoverageReport = {}

    for service, profile_entries in profile.items():
        configured_entries = config.services.get(service, {})
        uncovered_endpoints = {
            entry: intensity
            for entry, intensity in profile_entries.items()
            if entry not in configured_entries
        }
        total_intensity = sum(profile_entries.values())
        uncovered_intensity = sum(uncovered_endpoints.values())

        report[service] = ServiceCoverage(
            total_intensity=total_intensity,
            covered_intensity=total_intensity - uncovered_intensity,
            uncovered_endpoints=uncovered_endpoints,
        )

    return report
