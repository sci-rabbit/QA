# QA API - Сервис вопросов и ответов

API-сервис для управления вопросами и ответами, построенный на FastAPI и PostgreSQL.

## Описание проекта

QA API - это RESTful API для системы вопросов и ответов. Сервис позволяет:

- Создавать и управлять вопросами
- Добавлять ответы к вопросам
- Получать вопросы со всеми ответами
- Удалять вопросы и ответы (с каскадным удалением)

### Основные возможности

- ✅ CRUD операции для вопросов и ответов
- ✅ Каскадное удаление ответов при удалении вопроса
- ✅ Валидация данных через Pydantic
- ✅ Автоматическая документация API (Swagger/ReDoc)
- ✅ Асинхронная работа с базой данных
- ✅ Покрытие тестами

## Быстрый старт с Docker Compose

### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта. Вы можете:

**Вариант 1:** Скопировать пример и отредактировать:
```bash
cp .env.example .env
```

Если вы просто скопировали .env.example можно сразу перейти к шагу #2

**Вариант 2:** Создать `.env` вручную со следующими переменными:
```env
DB__USER=postgres
DB__PASSWORD=postgres
DB__HOST=db
DB__PORT=5432
DB__NAME=qa_db
```

> **Примечание:** При использовании Docker Compose `DB__HOST` должен быть `db` (имя сервиса в docker-compose.yaml), а не `localhost`.

**Также необходимо обновить URL базы данных в `alembic.ini`:**

Откройте файл `alembic.ini` и найдите строку `sqlalchemy.url` (примерно строка 87). Обновите её в соответствии с вашими настройками:

```ini
sqlalchemy.url = postgresql://postgres:postgres@db:5432/qa_db
```

Где:
- `postgres` - значение `DB__USER` из `.env`
- `postgres` - значение `DB__PASSWORD` из `.env`
- `db` - имя сервиса БД из docker-compose.yaml (или `localhost` для локального запуска)
- `5432` - порт БД
- `qa_db` - значение `DB__NAME` из `.env`

### 2. Запуск проекта

Просто выполните команду:

```bash
docker compose up -d
```

Эта команда:
- Создаст и запустит контейнер PostgreSQL
- Соберет и запустит контейнер с API
- Применит миграции базы данных
- Запустит сервер на порту 8000

### 3. Проверка работы

После запуска API будет доступен по адресу: `http://localhost:8000`

Проверьте работоспособность:
```bash
curl http://localhost:8000/health
```

Или откройте в браузере:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 4. Остановка проекта

```bash
docker compose down
```

Для полной очистки (включая данные БД):
```bash
docker compose down -v
```

## API Endpoints

### Вопросы (Questions)

- `GET /api/questions/` - список всех вопросов
- `POST /api/questions/` - создать новый вопрос
- `GET /api/questions/{id}` - получить вопрос и все ответы на него
- `DELETE /api/questions/{id}` - удалить вопрос (вместе с ответами)

### Ответы (Answers)

- `POST /api/questions/{id}/answers/` - добавить ответ к вопросу
- `GET /api/answers/{id}` - получить конкретный ответ
- `DELETE /api/answers/{id}` - удалить ответ

### Health Check

- `GET /health` - проверка работоспособности сервиса

## Примеры использования

### Создание вопроса

```bash
curl -X POST "http://localhost:8000/api/questions/" \
  -H "Content-Type: application/json" \
  -d '{"text": "What is Python?"}'
```

### Создание ответа

```bash
curl -X POST "http://localhost:8000/api/questions/1/answers/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Python is a programming language", "user_id": "user-123"}'
```

### Получение вопроса с ответами

```bash
curl "http://localhost:8000/api/questions/1"
```

## Запуск без Docker (для разработки)

### Требования

- Python 3.12+
- Poetry (для управления зависимостями)
- PostgreSQL 12+

### Установка

```bash
# Установка зависимостей
poetry install


### Настройка

1. Создайте файл `.env`:
```env
DB__USER=your_db_user
DB__PASSWORD=your_db_password
DB__HOST=localhost
DB__PORT=5432
DB__NAME=qa_db
```

2. Создайте базу данных и примените миграции:
```bash
createdb qa_db
alembic upgrade head
```

### Запуск

```bash
python main.py
```

Или через uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest tests/test_question_api.py

# С покрытием кода
pytest --cov=core --cov=api --cov-report=html
```

## Структура проекта

```
QA/
├── alembic/              # Миграции базы данных
├── api/                  # API endpoints
│   ├── views/           # Роутеры
│   └── dependencies.py # Зависимости FastAPI
├── core/                # Основная логика
│   ├── models/          # SQLAlchemy модели
│   ├── repositories/    # Репозитории для работы с БД
│   ├── schemas/         # Pydantic схемы
│   ├── services/        # Бизнес-логика
│   ├── config.py        # Конфигурация
│   └── database.py      # Настройка БД
├── tests/               # Тесты
├── main.py              # Точка входа приложения
├── Dockerfile           # Образ для контейнера
├── docker-compose.yaml  # Конфигурация Docker Compose
├── entrypoint.sh        # Скрипт запуска в контейнере
└── pyproject.toml       # Зависимости проекта
```


## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - реляционная база данных
- **Alembic** - миграции базы данных
- **Pydantic** - валидация данных
- **Pytest** - тестирование
