# Тесты для QA API

## Установка зависимостей

```bash
poetry install --with dev
```

## Запуск тестов

### Все тесты
```bash
pytest
```

### С подробным выводом
```bash
pytest -v
```

### Конкретный файл
```bash
pytest tests/test_question_api.py
```

### Конкретный тест
```bash
pytest tests/test_question_api.py::test_create_question_api
```

### С покрытием кода
```bash
pytest --cov=core --cov=api --cov-report=html
```

## Структура тестов

- `conftest.py` - фикстуры для тестовой БД и клиента
- `test_question_repository.py` - тесты репозитория вопросов
- `test_answer_repository.py` - тесты репозитория ответов
- `test_question_service.py` - тесты сервиса вопросов
- `test_answer_service.py` - тесты сервиса ответов
- `test_question_api.py` - тесты API endpoints для вопросов
- `test_answer_api.py` - тесты API endpoints для ответов

## Что тестируется

### Репозитории
- CRUD операции
- Получение несуществующих записей
- Удаление записей

### Сервисы
- Бизнес-логика
- Валидация (проверка существования вопросов при создании ответов)
- Обработка ошибок (404 для несуществующих записей)

### API Endpoints
- Все HTTP методы (GET, POST, DELETE)
- Валидация входных данных
- Каскадное удаление (удаление ответов при удалении вопроса)
- Множественные ответы от одного пользователя



