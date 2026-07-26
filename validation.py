"""Проверки структуры исходного конфигурационного файла."""

from typing import Any


REQUIRED_ENTRY_FIELDS = {"endpoint", "type", "scripts"}


def validate_config_structure(config: Any) -> bool:
    """Проверить типы и обязательные поля исходного конфига."""
    if not isinstance(config, dict):
        print("Data must be a dictionary")
        return False

    for service, entries in config.items():
        if not isinstance(service, str):
            print("Data key must be a string")
            return False
        if not isinstance(entries, list):
            print("Data value must be a list")
            return False

        for entry in entries:
            if not isinstance(entry, dict):
                print("Data list value must be a dictionary")
                return False
            if not REQUIRED_ENTRY_FIELDS.issubset(entry):
                print(
                    "Data list value must contain:\n"
                    "\tendpoint: str\n"
                    "\ttype: str\n"
                    "\tscripts: list[str]"
                )
                return False
            if not isinstance(entry["type"], str) or not entry["type"].strip():
                print("Data type must be a non-empty string")
                return False
            if not isinstance(entry["endpoint"], str) or not entry["endpoint"].strip():
                print("Data endpoint must be a non-empty string")
                return False
            if not isinstance(entry["scripts"], list):
                print("Data scripts must be a list")
                return False
            if not all(isinstance(script, str) for script in entry["scripts"]):
                print("Data scripts value must be a string")
                return False

    return True
