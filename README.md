# Для запуска приложения необходимо создать файл ".env" и установить в него переменные окружения:

- APP_SENTRY_URL
- APP_PORT
- APP_SECRET_KEY
- APP_ALGORITHM
- DB_HOST
- DB_USER
- DB_PASS
- DB_NAME
- DB_PORT
- JWT_REFRESH_TOKEN_NAME
- JWT_ACCESS_TOKEN_NAME

# Необходимо создать два ключа для работы авторизации в приложении, но для теста я создал два изначально: 

    openssl genrsa -out jwt-private.pem 2048

    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem


# Выполнить команду:
    
    docker compose up --build
    
# После разворачивания контейнеров можно выполнить миграции в контейнере приложения (app)

    alembic revision --autogenerate -m 'initial'

    alembic upgrade head
