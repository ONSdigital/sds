FROM python:3.11
COPY . src
RUN pip install functions-framework
RUN pip install firebase_admin
WORKDIR /src
ENV PYTHONPATH=src
CMD functions-framework --target dev_publish_dataset --debug