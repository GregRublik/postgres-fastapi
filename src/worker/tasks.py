from selery_app import app

@app.task
def process_message(message):
    """Пример задачи для обработки сообщения из RabbitMQ"""
    print(f"Получено сообщение: {message}")
    # Здесь ваша логика обработки
    return f"Обработано: {message}"
