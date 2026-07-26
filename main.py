"""CLI-приложение обработки конфигурации профилей нагрузочного тестирования."""

import argparse
import json
from pathlib import Path
from typing import Sequence

from conflicts import (
    find_endpoint_template_conflicts,
    find_script_conflicts,
    merge_endpoint_template_conflicts,
    print_endpoint_template_conflicts,
    print_script_conflicts,
)
from file_io import load_text, save_text
from normalization import ConfigNormalized, normalize_config
from validation import validate_config_structure


DEFAULT_SOURCE_PATH = Path("configs/config.json")
DEFAULT_OUTPUT_PATH = Path("configs/new_config.json")
CONTINUE_COMMANDS = {"y", "yes", "д", "да", "continue", "продолжить"}
STOP_COMMANDS = {"n", "no", "н", "нет", "stop", "остановиться", "exit", "выход"}


def build_argument_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description=(
            "Проверить, нормализовать и сохранить конфигурацию профилей НТ. "
            "Относительные пути вычисляются от текущей рабочей директории."
        )
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
        help=f"путь к исходному JSON-конфигу (по умолчанию: {DEFAULT_SOURCE_PATH})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"путь для результата (по умолчанию: {DEFAULT_OUTPUT_PATH})",
    )
    return parser


def ask_to_continue(prompt: str) -> bool:
    """Запросить у пользователя решение продолжить или остановить обработку."""
    while True:
        try:
            command = input(f"{prompt} [да/нет]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nОбработка остановлена.")
            return False

        if command in CONTINUE_COMMANDS:
            return True
        if command in STOP_COMMANDS:
            return False

        print("Введите 'да' для продолжения или 'нет' для остановки.")


def load_and_normalize_config(source_path: Path) -> ConfigNormalized | None:
    """Загрузить JSON, проверить его структуру и привести к единому виду."""
    try:
        source_config = json.loads(load_text(source_path))
    except OSError as error:
        print(f"Не удалось прочитать конфиг '{source_path}': {error}")
        return None
    except json.JSONDecodeError as error:
        print(f"Некорректный JSON в '{source_path}': {error}")
        return None

    if not validate_config_structure(source_config):
        return None

    try:
        return normalize_config(source_config)
    except ValueError as error:
        print(error)
        return None


def process_config(source_path: Path, output_path: Path) -> bool:
    """Выполнить интерактивную обработку конфига и сохранить результат."""
    normalized_config = load_and_normalize_config(source_path)
    if normalized_config is None:
        return False

    script_conflicts = find_script_conflicts(normalized_config)
    print_script_conflicts(script_conflicts)
    if script_conflicts and not ask_to_continue(
        "Продолжить, несмотря на пересечения скриптов?"
    ):
        print("Обработка остановлена на проверке скриптов.")
        return False

    template_conflicts = find_endpoint_template_conflicts(normalized_config)
    print_endpoint_template_conflicts(template_conflicts)
    if template_conflicts:
        if not ask_to_continue(
            "Объединить совпавшие endpoint в шаблоны и продолжить?"
        ):
            print("Обработка остановлена на проверке шаблонов.")
            return False
        merge_endpoint_template_conflicts(normalized_config, template_conflicts)
        print("Конкретные endpoint объединены с шаблонными.")

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_text(
            output_path,
            json.dumps(normalized_config, indent=4, ensure_ascii=False),
        )
    except OSError as error:
        print(f"Не удалось сохранить результат в '{output_path}': {error}")
        return False

    print(f"Результат сохранён: {output_path}")
    return True


def main(arguments: Sequence[str] | None = None) -> int:
    """Разобрать CLI-аргументы и вернуть код завершения программы."""
    args = build_argument_parser().parse_args(arguments)
    return 0 if process_config(args.config, args.output) else 1


if __name__ == "__main__":
    raise SystemExit(main())
