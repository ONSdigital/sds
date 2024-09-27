FROM python:3.11-alpine

RUN apt-get update && apt-get install -y make gcc
COPY . .
RUN pip install -r requirements.txt
RUN make unit-test
ENV PYTHONPATH=src
CMD exec uvicorn src.app:app --host 0.0.0.0 --port $PORT