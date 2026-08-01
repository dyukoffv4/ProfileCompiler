"""Модели отчёта о покрытии интенсивности."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceCoverage:
    """Статистика покрытия эндпоинтов одного сервиса."""

    total_intensity: int
    covered_intensity: int
    uncovered_endpoints: dict[str, int]

    @property
    def coverage_percent(self) -> float:
        """Вернуть процент покрытой интенсивности."""
        if self.total_intensity == 0:
            return 100.0
        return self.covered_intensity / self.total_intensity * 100


CoverageReport = dict[str, ServiceCoverage]
