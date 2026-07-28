"""Проверки структуры исходного конфигурационного файла."""

from typing import Any

REQUIRED_ENTRY_FIELDS = {"endpoint", "type", "scripts"}


def validate_config_structure(config: Any) -> bool:
    """Проверить типы и обязательные поля исходного конфига."""
    if not isinstance(config, dict):
        print("Data must be a dictionary")
        return False

    main = config.get("main", config)
    if not isinstance(main, dict):
        print("Main config must be a dictionary")
        return False

    for service, entries in main.items():
        if not isinstance(service, str) or not isinstance(entries, list):
            print("Invalid service structure")
            return False
        for entry in entries:
            if not isinstance(entry, dict) or not REQUIRED_ENTRY_FIELDS.issubset(entry):
                print("Invalid entry structure")
                return False
            if not isinstance(entry["type"], str) or not entry["type"].strip():
                print("Data type must be a non-empty string")
                return False
            if not isinstance(entry["endpoint"], str) or not entry["endpoint"].strip():
                print("Data endpoint must be a non-empty string")
                return False
            if not isinstance(entry["scripts"], list) or not all(isinstance(x, str) for x in entry["scripts"]):
                print("Data scripts value must be a string")
                return False

    statics = config.get("statics", {})
    if not isinstance(statics, dict) or not all(isinstance(k, str) and isinstance(v, int) for k, v in statics.items()):
        print("Statics must be a dictionary of script: value")
        return False

    return True
