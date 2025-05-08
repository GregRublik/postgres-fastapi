FROM python:3.12.4-slim

WORKDIR app/

COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry и зависимости
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main,celery --no-interaction --no-ansi

# Копируем исходный код
COPY worker/* src/config.py .env .test.env ./

CMD ["celery", "-A", "selery_app", "worker", "--loglevel=info", "-Q", "first_message"]
