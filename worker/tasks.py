from selery_app import app


@app.task(
    name='string',
    queue='first_message',
    bind=True,
    max_retries=3
)
def process_message(self, message):
    print(self.request)
    print(f"Received message: {message}")
    return {"status": "success", "message": message}
