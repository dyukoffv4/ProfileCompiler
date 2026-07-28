"""Публичный API командного интерфейса приложения."""

from .arguments import DEFAULT_OUTPUT_PATH, DEFAULT_SOURCE_PATH, build_argument_parser
from .prompts import CONTINUE_COMMANDS, STOP_COMMANDS, ask_confirmation
from .entrypoint import main

__all__ = [
    "CONTINUE_COMMANDS",
    "DEFAULT_OUTPUT_PATH",
    "DEFAULT_SOURCE_PATH",
    "STOP_COMMANDS",
    "ask_confirmation",
    "build_argument_parser",
    "main",
]
