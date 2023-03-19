FROM python:3.11
COPY ../src/app src
COPY ../requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /src
ENV PYTHONPATH=src
CMD functions-framework --target new_dataset --debug