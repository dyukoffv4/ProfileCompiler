"""Сценарий анализа и вывода покрытия интенсивности."""

from domain.configuration import ConfigNormalized
from domain.coverage import CoverageReport, calculate_coverage
from domain.profile import ProfileNormalized


def run_coverage_analysis(profile: ProfileNormalized, config: ConfigNormalized) -> CoverageReport:
    """Рассчитать покрытие, вывести отчёт и вернуть его вызывающему сценарию."""
    report = calculate_coverage(profile, config)

    print("\nПокрытие интенсивности по сервисам:")
    for service, coverage in report.items():
        print(
            f"- {service}: {coverage.covered_intensity} из {coverage.total_intensity} ({coverage.coverage_percent:.2f}%)")

        if coverage.uncovered_endpoints:
            print("  Непокрытые эндпоинты:")
            for endpoint, intensity in coverage.uncovered_endpoints.items():
                print(f"\t- {endpoint}: {intensity}")
        else:
            print("  Все эндпоинты покрыты конфигом.")

    return report
