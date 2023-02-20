# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

* https://confluence.ons.gov.uk/display/SDC/SDS

## Running locally

To run this service locally, you will need the following:

* Python 3.11
* Docker or credentials for GCloud

You will need to make a choice to run with either GCP service emulators or the real thing.
Instructions for setting up both are included below.

### Setting up a virtual environment

Check that you have the correct version of Python installed and then run the following commands:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

### Connecting to services running in GCloud

In order to connect to real services in GCloud, you will need a key file. To create one:

* Go the IAM page and select Service accounts
* Create a new service account
* Call it "test"
* Add whatever roles are needed for testing. "Owner" will work but this is potentially too much access
* Go into service account and create a key. This will download a JSON file to your machine
 
Copy the downloaded JSON file to this director and rename to `key.json` and set the following environment variable:

```bash
export KEYFILE_LOCATION=key.json
```

### Connecting to the emulators

The Firestore emulator runs in Docker and the Google Cloud Storage emulator runs locally as part of the integration
tests. To connect to the Firestore emulator running locally in Docker, run the following commands:


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