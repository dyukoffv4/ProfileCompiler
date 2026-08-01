"""Точка входа CLI-приложения профилей нагрузочного тестирования."""

from collections.abc import Sequence

from application.workflows import process

from .arguments import build_argument_parser


def main(arguments: Sequence[str] | None = None) -> int:
    """Разобрать аргументы CLI, запустить обработку и вернуть код завершения."""
    args = build_argument_parser().parse_args(arguments)
    return 0 if process(args.config, args.config_output, args.profile, args.profile_output) else 1


if __name__ == "__main__":
    raise SystemExit(main())
