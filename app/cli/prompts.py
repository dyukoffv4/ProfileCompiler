"""Интерактивные запросы CLI."""

CONTINUE_COMMANDS = {"y", "yes", "д", "да", "continue", "продолжить"}
STOP_COMMANDS = {"n", "no", "н", "нет", "stop", "остановиться", "exit", "выход"}


def ask_confirmation(prompt: str) -> bool:
    """Запросить у пользователя подтверждение действия."""
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

        print("Введите 'да' для подтверждения или 'нет' для отказа.")


def ask_to_continue(prompt: str) -> bool:
    """Запросить решение продолжить или остановить обработку."""
    return ask_confirmation(prompt)


def ask_to_save(prompt: str = "Сохранить обработанный конфиг?") -> bool:
    """Запросить подтверждение сохранения результата."""
    return ask_confirmation(prompt)
