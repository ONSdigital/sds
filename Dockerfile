FROM python:3.11-alpine
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/app src
ENV PYTHONPATH=src
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "echo", "$PORT"]