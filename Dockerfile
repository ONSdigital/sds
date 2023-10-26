FROM alpine:latest
ARG PYTHON_VERSION=3.12.0
COPY src/app src
COPY requirements.txt requirements.txt
RUN python3 get-pip.py
RUN pip install -r requirements.txt
ENV PYTHONPATH=src
CMD exec uvicorn src.app:app --host 0.0.0.0 --port $PORT
