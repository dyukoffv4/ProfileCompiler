"""Последовательность интерактивных проверок конфигурации."""

from configuration import ConfigNormalized
from conflicts import (
    find_endpoint_template_conflicts,
    find_script_conflicts,
    merge_endpoint_template_conflicts,
    print_endpoint_template_conflicts,
    print_script_conflicts,
)

from app.cli.prompts import ask_confirmation


def run_conflict_checks(config: ConfigNormalized) -> bool:
    """Провести проверки конфликтов и применить выбранные исправления."""
    script_conflicts = find_script_conflicts(config)
    print_script_conflicts(script_conflicts)
    if script_conflicts and not ask_confirmation("Продолжить, несмотря на пересечения скриптов?"):
        print("Обработка остановлена на проверке скриптов.")
        return False

    template_conflicts = find_endpoint_template_conflicts(config)
    print_endpoint_template_conflicts(template_conflicts)
    if not template_conflicts:
        return True

    if not ask_confirmation("Объединить совпавшие endpoint в шаблоны и продолжить?"):
        print("Обработка остановлена на проверке шаблонов.")
        return False

    merge_endpoint_template_conflicts(config, template_conflicts)
    print("Конкретные endpoint объединены с шаблонными.")
    return True
