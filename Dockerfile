FROM python:3.11-alpine
COPY src/app src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH=src
CMD exec uvicorn src.app:app --host 0.0.0.0 --port $PORT --workers 80