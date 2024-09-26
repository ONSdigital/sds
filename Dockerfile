FROM python:3.11-alpine AS builder
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/app src

FROM python:3.11-alpine
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder src src
ENV PYTHONPATH=src
CMD exec uvicorn src.app:app --host 0.0.0.0 --port $PORT
