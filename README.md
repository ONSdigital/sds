# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

* https://confluence.ons.gov.uk/display/SDC/SDS

## Running locally

To run this service locally, you will need the following:

* Python 3.11
* Docker or credentials for GCloud

You will need to make a choice to run with either the Firestore emulator or a real firestore instance.
Instructions for setting up both are included below.

### Setting up a virtual environment

Check that you have the correct version of Python installed and then run the following commands:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

### Connecting to Firestore running in GCloud

In order to create the credentials, watch https://www.youtube.com/watch?v=MU7O6emzAc0 .

Put the credentials in a file called `firebase_key.json` and set the following environment variable:

```bash
export KEYFILE_LOCATION=firebase_key.json
```

### Connecting to the Firestore emulator

To connect to the emulator running locally in Docker, run the following commands:


```bash
docker-compose up -d firestore
unset KEYFILE_LOCATION
export FIRESTORE_EMULATOR_HOST=localhost:8200
```

### Run SDS locally

To run SDS locally, activate the virtual environment, export the appropriate environment variables (see above)
then run the following commands:

```bash
export PYTHONPATH=src/app
python -m uvicorn src.app.app:app --reload --port 8013
```

## Running linting and unit tests locally

To run all the checks that run as part of the CI, run the following commands:

```
black . --check
isort . --check-only --profile black
flake8 src --max-line-length=127
export PYTHONPATH=src/app
pytest --cov=src/app src/unit_tests
coverage report --fail-under=90
```

To correct any problems that `isort` or `black` complain about, run the following:

```
black .
isort . --profile black
```

## Building and running on Docker

To build and run on docker, run the following commands:

```bash
docker-compose build
docker-compose up
```

## OpenAPI Specification

As this runs in FastAPI, the Open API Spec and interactive API docs are auto-generated from the Python code and
can be reached by going to the following URLs (once running):

* http://localhost:8000/openapi.json
* http://localhost:8000/docs

## Running the integration tests

The integration tests in `src/integration_tests/local_tests.py` require a database and like the app, can be run
against a real database or the emulator. This tests will auto-switch between the firestore emulator
and the real Firestore, depending on whether firebase_key.json present. If this file is not present and the emulator
is not running it will fail with a useful message. To run the tests, run the following:

```
cd src/integration_tests
export PYTHONPATH=../app
pytest local_tests.py
```

# Contact

* mike.tidman@ons.gov.uk