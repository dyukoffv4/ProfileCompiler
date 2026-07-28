"""Инфраструктурный слой приложения."""

from .storage import load_csv, load_json, load_text, save_csv, save_json, save_text

__all__ = [
    "load_csv",
    "load_json",
    "load_text",
    "save_csv",
    "save_json",
    "save_text",
]
