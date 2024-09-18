FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN apk add --no-cache gcc musl-dev libffi-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/app src
ENV PYTHONPATH=src
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "$PORT"]