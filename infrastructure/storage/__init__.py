"""Публичный API файлового хранилища."""

from .csv_files import load_csv, save_csv
from .json_files import load_json, save_json
from .text_files import load_text, save_text

__all__ = [
    "load_csv",
    "load_json",
    "load_text",
    "save_csv",
    "save_json",
    "save_text",
]
