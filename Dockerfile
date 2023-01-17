FROM python:3.11
COPY src src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY firebase_key.json firebase_key.json
ENV PYTHONPATH=src
CMD exec uvicorn src.app:app --reload --host 0.0.0.0 --port $PORT
