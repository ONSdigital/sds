FROM python:3.11-slim
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src/app src
ENV PYTHONPATH=src
CMD ["fastapi", "run", "app/main.py", "--port", "$PORT"]