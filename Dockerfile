FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/


RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi


COPY . /app/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python main.py"]
