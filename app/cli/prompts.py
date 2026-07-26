"""Интерактивные запросы CLI."""

CONTINUE_COMMANDS = {"y", "yes", "д", "да", "continue", "продолжить"}
STOP_COMMANDS = {"n", "no", "н", "нет", "stop", "остановиться", "exit", "выход"}


def ask_to_continue(prompt: str) -> bool:
    """Запросить решение продолжить или остановить обработку."""
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
