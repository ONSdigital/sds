# Supplementary Data Service (sds)

Information on the service can be found on Confluence:

* https://confluence.ons.gov.uk/display/SDC/SDS

## Running locally

To run this service locally, you will need the following:

* Python 3.11
* VirtualEnv
* Docker

### Creating, activating and deactivating a Python virtual environment

Check that you have the correct version of Python installed and then run the following commands:

```
virtualenv venv
source venv/bin/activate
```

This will create and activate the virtual environment. To deactivate the environment, run the following command:

```
deactivate
```

### Installing the dependencies

Assuming that the virtual environment is activated, run the following command:

```
pip install -r requirement.txt
```

### Storing environment variables

Git is configured to ignore the `local.env` file. If you want to use another file to store environment variables then please add the file name to the `.gitignore` file in the repository root. At the very least you need to include the following:

```
FIRESTORE_PROJECT_ID=localhost
FIRESTORE_EMULATOR_HOST=localhost:8200

GOOGLE_APPLICATION_CREDENTIALS=local_firebase_credentials.json

FIREBASE_KEYFILE_LOCATION=firebase_key.json
```

Note that the `FIRESTORE_PROJECT_ID` and `FIRESTORE_EMULATOR_HOST` environment variables match the settings in the `docker-compose.yml` file. The other two are covered in a later subsection.

### Installing and running Firestore with Docker

In order to install the Firestore emulator, and assuming that you have Docker installed, run the following command:

```
docker-compouse up -d firestore
```

And to check that the container is running:

```
docker ps
```

To subsequently stop and start the container, run the following commands respectively:

```
docker start firestore
docker stop firestore
```

To delete the container once and for all, whether currently running or not, run the following command:

```
docker-compose down
```

The `docker` commands can be run anywhere. The `docker-compose` commands should be run from the repository root so that the Docker compose file can be found, unless you want to explicitly specify its path.

### Connecting to the Firestore instance

There is a `scratch.py` file that can be run 












## Miscellaneous


https://github.com/firebase/firebase-admin-python/blob/master/tests/data/service_account.json

https://groups.google.com/g/firebase-talk/c/IKo6PsXMqlQ


* A Google Firebase key file (see https://www.youtube.com/watch?v=MU7O6emzAc0)
* Docker or Rancher desktop (optional but needed if you want to run the docker image)

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

# Running integration tests

The integration tests can be run locally but don't currently work on a CI environment. Unlike the unit tests,
the integration tests require credentials to connect to a Firestore database. In the future, communicating with a 
real Cloud Firestore database could be replaced with https://cloud.google.com/firestore/docs/emulator for integration
testing purposes, which may also then open the possibility of running the integration tests in CI or folding them
into the unit test suit.

To run the integration tests, ensure you have a Firebase key file and then do the following:

```bash
cd integration_tests
export PYTHONPATH=../src
pytest
```