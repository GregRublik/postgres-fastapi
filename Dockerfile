FROM python:3.12.4

WORKDIR app/

COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry и зависимости
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main,dev --no-interaction --no-ansi

COPY . .

#CMD alembic revision --autogenerate -m 'initial' && alembic upgrade head

CMD python src/app.py
