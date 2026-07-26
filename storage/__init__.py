"""Операции чтения и записи файлов."""

from .csv_files import load_csv, save_csv
from .json_files import load_json, save_json
from .text_files import load_text, save_text

__all__ = ["load_csv", "save_csv", "load_json", "save_json", "load_text", "save_text"]
