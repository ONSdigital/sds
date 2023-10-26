FROM alpine:latest
ARG PYTHON_VERSION=3.12.0
COPY src/app src
COPY requirements.txt requirements.txt

# Install Python and pip
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    python3 -m pip install --upgrade pip && \
    ln -s /usr/bin/python3 /usr/bin/python \

RUN pip install -r requirements.txt
ENV PYTHONPATH=src
CMD exec uvicorn src.app:app --host 0.0.0.0 --port $PORT
