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

### Running SDS locally with services running in GCloud

In order to connect to real services in GCloud, you will need a GCP test project or make
use of the sandbox project. Instructions for setting this up  are included in the IaC repo. 
You will need to take note of the schema and dataset bucket names for the project you are using.

Once you have setup your project, you will need a key file to allow SDS to talk to bucket storage
and the database. To create one:

* Go the IAM page and select Service accounts
* Create a new service account
* Call it "test"
* Add the roles that are needed for testing
* Go into service account and create a key. This will download a JSON file to your machine 
* Copy the downloaded JSON file to this directory and rename to `key.json`

To run SDS locally, activate the virtual environment, then run the following commands (replacing `my-schema-bucket`
and `dataset-bucket` appropriately:

```bash
export PYTHONPATH=src/app
export SCHEMA_BUCKET_NAME=my-schema-bucket
export DATASET_BUCKET_NAME=my-dataset-bucket
export GOOGLE_APPLICATION_CREDENTIALS=key.json
python -m uvicorn src.app.app:app --reload --port 8013
```

### Running the SDS with service emulators

The Firestore and Cloud Storage emulators run in Docker. To connect to the Firestore emulator running locally in Docker,
run the following commands:


```bash
docker-compose up -d firestore
docker-compose up -d storage
export FIRESTORE_EMULATOR_HOST=localhost:8200
export STORAGE_EMULATOR_HOST=http://localhost:9023
export PYTHONPATH=src/app
python -m uvicorn src.app.app:app --reload --port 8013
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

## new_dataset loud Function

`new_dataset` runs as a Cloud Function. It is Triggered by uploading a new dataset file to the dataset storage bucket.
To deploy the Cloud Function, run the following locally, but set the DATASET_BUCKET environment variables first:

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME

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

## Running the integration tests

The integration tests will work in a number of different ways depending on how you want to test the SDS API service
and SDS cloud function. The following sections describe a number of combinations

### Everything running in the cloud

In this configuration, the SDS API service is running in Cloud Run and the new-dataset-function is deployed
to Cloud Functions on your test/dev GCP project. These services both talk to Firestore and Cloud Storage running
on the same project. This test configuration is also what is run at the end of the Cloud Build deployment.

Run them like this (replacing `https://sds-blahblah.a.run.app` with the actual cloud run endpoint and
`a-place-for-datasets` with the real dataset bucket):

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME

# To talk to the REST endpoint
export AUTH_TOKEN=$(gcloud auth print-identity-token)  
export CLOUD_RUN_ENDPOINT=https://sds-blahblah.a.run.app

# To talk to Cloud Storage
export DATASET_BUCKET=a-place-for-datasets  
export GOOGLE_APPLICATION_CREDENTIALS=../../key.json

cd src/integration_tests
pytest integration_tests.py
```

### SDS API service is local

This configuration allows you to debug the SDS API locally but talk to real Google services. Run them like this 
(replacing `my-schema-bucket` with the real schema bucket and `a-place-for-datasets` with the real dataset bucket):

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME

export SCHEMA_BUCKET_NAME=my-schema-bucket
export DATASET_BUCKET=a-place-for-datasets
export GOOGLE_APPLICATION_CREDENTIALS=../../key.json

export PYTHONPATH=../app
cd src/integration_tests
pytest integration_tests.py
```

### Everything is local

This configuration makes use of the firestore and storage services running in Docker. The cloud function behaviour
is emulated by the test itself.

```bash
docker-compose up -d firestore
docker-compose up -d storage

export FIRESTORE_EMULATOR_HOST=localhost:8200
export STORAGE_EMULATOR_HOST=http://localhost:9023
export SCHEMA_BUCKET_NAME=schema-bucket
export DATASET_BUCKET=dataset-bucket

export PYTHONPATH=../app
cd src/integration_tests
pytest integration_tests.py
```

# Contact

* mike.tidman@ons.gov.uk