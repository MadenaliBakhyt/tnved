# ТН ВЭД API

API для поиска информации по коду ТН ВЭД (Товарная номенклатура внешнеэкономической деятельности).

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Импорт данных из Excel

```bash
python import_excel.py tnved.xlsx
```

Скрипт автоматически создаёт базу данных SQLite в `data/tnved.db`. При повторном запуске данные полностью заменяются.

## Запуск API

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

## Запуск через Docker

```bash
# Сначала импортируйте данные локально или положите готовую БД в data/
docker compose up -d
```

## API Endpoints

### Поиск по коду

```
GET /code/{code}
```

Пример:
```bash
curl http://localhost:8000/code/9705220000
```

Ответ:
```json
{
  "code": "9705220000",
  "name": "...",
  "tariff": "0%",
  "details": "...",
  "unit": "...",
  "notes": "..."
}
```

### Поиск по наименованию

```
GET /search?q=молоко&limit=10
```

Ответ:
```json
{
  "total": 5,
  "results": [
    {
      "code": "...",
      "name": "...",
      "tariff": "...",
      "details": "...",
      "unit": "...",
      "notes": "..."
    }
  ]
}
```

### Проверка здоровья

```
GET /health
```

## Swagger документация

После запуска доступна по адресу:

```
http://localhost:8000/docs
```

## Конфигурация

Через файл `.env`:

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DATABASE_URL` | Путь к SQLite базе | `sqlite:///data/tnved.db` |
| `SEARCH_LIMIT` | Лимит результатов поиска | `50` |
