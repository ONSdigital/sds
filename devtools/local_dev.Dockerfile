FROM python:3.11
COPY ../src src
COPY ../requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH=src
WORKDIR /src
CMD exec uvicorn app:app --reload --host 0.0.0.0 --port $PORT