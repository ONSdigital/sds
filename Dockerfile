FROM ghcr.io/astral-sh/uv:python3.13-alpine
COPY pyproject.toml .
RUN pip install -r requirements.txt
COPY src/app src
ENV PYTHONPATH=src
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port $PORT"]