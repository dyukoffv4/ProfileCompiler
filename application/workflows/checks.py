"""Последовательность интерактивных проверок конфигурации."""

from domain.configuration import ConfigNormalized
from domain.conflicts import find_endpoint_template_conflicts, find_script_conflicts, print_endpoint_template_conflicts, print_script_conflicts
from domain.conflicts.scripts import find_static_script_conflicts
from application.cli.prompts import ask_confirmation


def run_conflict_checks(config: ConfigNormalized) -> bool:
    script_conflicts = find_script_conflicts(config)
    print_script_conflicts(script_conflicts)

    if script_conflicts and not ask_confirmation("Продолжить, несмотря на пересечения скриптов?"):
        return False
    print()

    static_conflicts = find_static_script_conflicts(config)

    if static_conflicts:
        print("Пересечения статичных скриптов с основными:")
        print("\n".join(f"\t{x}" for x in static_conflicts))
        if not ask_confirmation("Продолжить, несмотря на пересечения статичных скриптов?"):
            return False
    print()

    template_conflicts = find_endpoint_template_conflicts(config)
    print_endpoint_template_conflicts(template_conflicts)

    return not template_conflicts or ask_confirmation("Продолжить, несмотря на совпавшие endpoint?")
