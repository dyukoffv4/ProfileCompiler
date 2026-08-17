"""Последовательность проверок конфигурации."""

from application.cli.prompts import ask_confirmation
from domain.configuration import ConfigNormalized
from domain.conflicts import (
    find_endpoint_template_conflicts,
    find_script_conflicts,
    print_endpoint_template_conflicts,
    print_script_conflicts
)


def run_conflict_checks(config: ConfigNormalized) -> bool:
    """Проверить допустимые пересечения конфигурации.

    Повторы скриптов между разными endpoint допустимы: их интенсивности
    суммируются, поэтому здесь выводится предупреждение. Фатальные пересечения
    скриптов проверяются во время нормализации конфига.
    """
    template_conflicts = find_endpoint_template_conflicts(config)
    print_endpoint_template_conflicts(template_conflicts)
    if template_conflicts and not ask_confirmation("Продолжить, несмотря на совпавшие endpoint?"):
        return False
    print()

    script_conflicts = find_script_conflicts(config)
    print_script_conflicts(script_conflicts)
    if script_conflicts and not ask_confirmation("Продолжить, несмотря на пересечения скриптов?"):
        return False

    return True
