# Background

This is the repo for the Supplementary Data Service (SDS), which is described in 
https://confluence.ons.gov.uk/display/SDC/SDS

# Running locally

To run this service locally, you will need the following:

* Python 3.11
* A Google Firebase key file (see https://www.youtube.com/watch?v=MU7O6emzAc0)
* Docker or Rancher desktop (optional but needed if you want to run the docker image)

To run, set up a local virtual environment and install the libraries described in the requirements file (see below).

```bash
python venv .venv
. .venv/bin/activate
pip install -r requirement.txt
```

Copy the firebase key file to `firebase_key.json` (in this directory) and run the `run.sh` file in (in the virtual
environment).

## Running linting and unit tests

To run all the checks that run as part of the CI, run the following:

```bash
black . --check
isort . --check-only --profile black
flake8 src integration_tests --max-line-length=127
export PYTHONPATH=src
pytest --cov=src src
coverage report --fail-under=90
```

To correct any problems that `isort` or `black` complain about, run the following:

```bash
black .
isort . --profile black
```

## Building and running on Docker

To build and run on docker, run the following commands:

```bash
docker-compose build
docker-compose up
```

# OpenAPI Specification

As this runs in FastAPI, the Open API Spec and interactive API docs are auto-generated from the Python code and
can be reached by going to the following URLs (once running):

* http://localhost:8000/openapi.json
* http://localhost:8000/docs
