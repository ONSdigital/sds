FROM python:3.11
COPY . src
RUN pip install fastapi==0.95.0
RUN pip install uvicorn==0.21.1
RUN pip install google-cloud-storage==2.7.0
RUN pip install requests==2.28.2
WORKDIR /src
ENV PYTHONPATH=src
CMD exec uvicorn app:app --reload --host 0.0.0.0 --port 8080