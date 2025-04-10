FROM python:3.12.4

WORKDIR app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD alembic revision --autogenerate -m 'initial' && alembic upgrade head

CMD python src/app.py
