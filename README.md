# ТН ВЭД Search API

Приложение для поиска информации по коду ТН ВЭД. Backend на FastAPI + PostgreSQL, frontend на React + TypeScript + TailwindCSS.

## Запуск через Docker

```bash
docker compose up -d
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Импорт данных из Excel

```bash
# При запущенном PostgreSQL (через Docker или локально)
cd backend
pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Импортировать данные
python import_excel.py tnved.xlsx
```

Формат Excel: первые 4 колонки — Код, Наименование, Тариф, Подробности. Все остальные колонки объединяются в массив документов.

## Локальный запуск без Docker

### PostgreSQL

Создать базу данных `tnved`:

```bash
createdb tnved
```

### Backend

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на http://localhost:5173, запросы к `/api` проксируются на backend.

## API

### Поиск по коду

```bash
curl http://localhost:8000/api/code/0101210000
```

```json
{
  "code": "0101210000",
  "name": "Лошади чистопородные",
  "tariff": "0%",
  "details": "подробнее",
  "documents": [
    "Внешнеэкономический контракт",
    "Коммерческий инвойс",
    "CMR"
  ]
}
```

### Поиск по наименованию

```bash
curl "http://localhost:8000/api/search?q=лошади"
```

```json
[
  {
    "code": "0101210000",
    "name": "Лошади чистопородные"
  }
]
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/tnved` |
| `SEARCH_LIMIT` | Лимит результатов поиска | `50` |
