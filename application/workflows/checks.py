"""Последовательность проверок конфигурации."""

from application.cli.prompts import ask_confirmation
from domain.configuration import ConfigNormalized
from domain.conflicts import find_endpoint_template_conflicts, print_endpoint_template_conflicts


def run_conflict_checks(config: ConfigNormalized) -> bool:
    """Проверить пересечения endpoint-шаблонов.

    Фатальные пересечения скриптов проверяются во время нормализации конфига.
    """
    template_conflicts = find_endpoint_template_conflicts(config)
    print_endpoint_template_conflicts(template_conflicts)

    return not template_conflicts or ask_confirmation("Продолжить, несмотря на совпавшие endpoint?")
