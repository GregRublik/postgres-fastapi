from selery_app import app


@app.task(
    bind=True,
    queue="first_message"
)  # rate_limit="10/m"
def process_message(self, message):
    """
    Пример задачи для обработки сообщения из RabbitMQ
    SUCCESS - успешное завершение
    FAILURE - неудачное завершение
    PENDING - в ожидании
    RETRY - задача будет повторена
    REVOKED - задача отменена
    """
    try:
        print(f"id message: {self.request.id}, message: {message}")
        self.update_state(state='SUCCESS')
    except Exception:
        self.update_state(state='FAILURE')