"""Совместимая точка запуска CLI из корня проекта."""

from application.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
