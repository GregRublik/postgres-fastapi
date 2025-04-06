# FastAPI, SQLALCHEMY, ONION ARCHITECTURE, JWT
 * Данное приложение совмещает в себе fastapi, sqlalchemy, 
postgresql и представляет из себя базу для быстрого развертывания приложения с необходимым функционалом
 * Приложение построено на onion architecture, тут есть слои repository, schemas, services, routing.
 * Также разработана система авторизации пользователя.

# Launch
* необходимо создать файл ".env" следующие переменные:
    
  - APP_SENTRY_URL # в приложение подключен мониторинг в сервисе sentry
  - APP_PORT # порт на котором будет запускаться приложение 
  - DB_HOST  # Для запуска базы данных 
  - DB_USER  # Для запуска базы данных 
  - DB_PASS  # Для запуска базы данных 
  - DB_NAME  # Для запуска базы данных 
  - DB_PORT  # Для запуска базы данных 
  - JWT_REFRESH_TOKEN_NAME  # имя токена refresh
  - JWT_ACCESS_TOKEN_NAME  # имя токена access
  - JWT_ALGORITHM # тут используется "RS256" 


* Необходимо создать два ключа в корневой директории для работы авторизации в приложении, но для теста я создал два изначально: 

    openssl genrsa -out jwt-private.pem 2048

    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem


* Выполнить команду:
    
    docker compose up --build
    
* После разворачивания контейнеров нужно создать и выполнить миграции в контейнере приложения (app)

    alembic revision --autogenerate -m 'initial'

    alembic upgrade head
