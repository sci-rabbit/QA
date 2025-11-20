#!/bin/sh
# entrypoint.sh

# Прогоняем миграции
alembic upgrade head

exec python main.py
