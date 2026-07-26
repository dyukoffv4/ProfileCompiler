# NT profile config tool

CLI-приложение для проверки, нормализации и сохранения конфигурации профилей нагрузочного тестирования.

## Запуск

```bash
python main.py --config configs/config.json --output configs/new_config.json
```

Без аргументов используются пути `configs/config.json` и `configs/new_config.json`.

## Структура

- `main.py` — минимальная точка входа;
- `app/cli` — аргументы и интерактивные запросы;
- `app/workflow` — загрузка, проверки и общий сценарий обработки;
- `configuration` — модели, валидация и нормализация;
- `conflicts` — модели и отдельные проверки конфликтов;
- `storage` — работа с JSON, CSV и текстовыми файлами.
