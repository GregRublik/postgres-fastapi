from selery_app import app


@app.task(name='string', queue='first_message')
def process_message(message):
    print(f"Received message: {message}")
    return {"status": "success", "message": message}
