# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

* https://confluence.ons.gov.uk/display/SDC/SDS

## Running locally

To run this service locally, you will need the following:

* Python 3.11
* Docker or credentials for GCloud

It is also strongly recommended you install the Google SDK (`brew install --cask google-cloud-sdk`)

You will need to make a choice to run with either GCP service emulators or the real thing.
Instructions for setting up both are included below.

### Setting up a virtual environment

Check that you have the correct version of Python installed and then run the following commands:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running SDS and integration tests with services running in GCloud

In order to connect to real services in GCloud, you will need a key file. To create one:

* Go the IAM page and select Service accounts
* Create a new service account
* Call it "test"
* Add whatever roles are needed for testing. "Owner" will work but this is potentially too much access
* Go into service account and create a key. This will download a JSON file to your machine 
* Copy the downloaded JSON file to this directory and rename to `key.json`

You will also need a bucket to put schema files in. Go to the Google Cloud Storage page and create this or 
refer to an existing one. Make a note of the name and replace `my-schema-bucket` with that name in these instructions.

To run SDS locally, activate the virtual environment, then run the following commands:

```bash
export PYTHONPATH=src/app
export SCHEMA_BUCKET_NAME=my-schema-bucket
export GOOGLE_APPLICATION_CREDENTIALS=key.json
python -m uvicorn src.app.app:app --reload --port 8013
```

There are a set of integration tests that allow you to debug SDS but can talk to real Google services. The following
commands will run those:

```bash
cd src/integration_tests
export PYTHONPATH=../app
export SCHEMA_BUCKET_NAME=my-schema-bucket
pytest local_tests.py
```



### Running SDS and integration tests with service emulators

The Firestore and Cloud Storage emulator run in Docker. To connect to the Firestore emulator running locally in Docker,
run the following commands:


```bash
docker-compose up -d firestore
docker-compose up -d storage
export FIRESTORE_EMULATOR_HOST=localhost:8200
export STORAGE_EMULATOR_HOST=http://localhost:9023
export PYTHONPATH=src/app
python -m uvicorn src.app.app:app --reload --port 8013
```

To run the debuggable integration tests with the emulator, run the following commands:

```bash
docker-compose up -d firestore
docker-compose up -d storage
cd src/integration_tests
export PYTHONPATH=../app
pytest local_tests.py
```

## Running linting and unit tests

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

## Cloud Functions

The Cloud Function setup is heavily based on https://cloud.google.com/functions/docs/tutorials/storage

To deploy the Cloud Functions, run the following locally, but set PROJECT_NAME and DATASET_BUCKET
environment variables first:

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME

PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format='value(project_number)')

SERVICE_ACCOUNT=$(gsutil kms serviceaccount -p $PROJECT_NUMBER)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SERVICE_ACCOUNT \
  --role roles/pubsub.publisher

cd src/app/

gcloud functions deploy new-dataset-function \
--gen2 \
--runtime=python311 \
--region=europe-west2 \
--source=. \
--entry-point=new_dataset \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=$DATASET_BUCKET"
```

## Cloud Run Tests

These are integration tests which make calls into SDS running on GCloud via the API. Run them like this
(replacing `https://sds-blahblah.a.run.app` with the actual cloud run endpoint and `a-place-for-datasets` with
the real dataset bucket):

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME
export AUTH_TOKEN=$(gcloud auth print-identity-token)
export CLOUD_RUN_ENDPOINT=https://sds-blahblah.a.run.app
export DATASET_BUCKET=a-place-for-datasets
export GOOGLE_APPLICATION_CREDENTIALS=../../key.json
cd src/integration_tests
pytest cloudrun_test.py
```

```bash
export FIRESTORE_EMULATOR_HOST=localhost:8200
export STORAGE_EMULATOR_HOST=http://localhost:9023
```


# Contact

* mike.tidman@ons.gov.uk