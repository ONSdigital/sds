# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

* https://confluence.ons.gov.uk/display/SDC/SDS
---
## Dockerized
The docker-compose will launch the SDS application, two storage emulators(firebase and bucket), the new_dataset cloud function and a supporting publish dataset endpoint. The SDS application will also support hot reloading within the `/src/app` directory.

- You will need to create a new file called `mock_google_app_key.json` within the `/devtools` directory and copy the contents from this fake service acount found here [Mock service account](https://github.com/firebase/firebase-admin-python/blob/master/tests/data/service_account.json).

```
docker-compose up
```
Once, loaded you can do the following:

- View the API service docs [localhost:3000/docs](http://localhost:3000/docs).

- See files put into cloud storage within `devtools/gcp-storage-emulator/data/default-bucket`.

- Utilize the firestore emulator [localhost:4000/firestore](http://localhost:4000/firestore).

- Simulate the SDX publish process, invoked with a dataset as follows.

```
curl -X POST localhost:3006 \
-H "Content-Type: application/cloudevents+json" \
-d '{ "survey_id": "NRX",
  "period_id": "ttt",
  "form_id": "yyy",
  "title": "Which side was better?",
  "sds_schema_version": 4,
  "schema_version": "v1.0.0",
  "data": [
    {
      "ruref": "43532",
      "runame": "Pipes and Maps Ltd",
      "local_unit": [
        {
          "luref": "2012763A",
          "luname": "Maps Factory"
        },
        {
          "luref": "20127364B",
          "luname": "Pipes R Us Subsidiary"
        }
      ]
    }
 ]
}'
```

---
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
python -m uvicorn src.app.app:app --reload --port 3000
```

### Running the SDS with service emulators

The Firestore and Cloud Storage emulators run in Docker. To connect to the Firestore emulator running locally in Docker,
run the following commands:


```bash
docker-compose up 
docker-compose stop api

export FIRESTORE_EMULATOR_HOST=localhost:8080
export STORAGE_EMULATOR_HOST=http://localhost:9023
export PYTHONPATH=src/app
python -m uvicorn src.app.app:app --reload --port 3000
```

## Running linting and unit tests

To run all the checks that run as part of the CI, run the following commands:

```
black . --check
isort . --check-only --profile black
flake8 src --max-line-length=127
cd src/unit_tests
export PYTHONPATH=../app
pytest --cov=../app .
coverage report --fail-under=90
```

To correct any problems that `isort` or `black` complain about, run the following:

```
black .
isort . --profile black
```

## OpenAPI Specification

As this runs in FastAPI, the Open API Spec and interactive API docs are auto-generated from the Python code and
can be reached by going to the following URLs (once running):

* http://localhost:8000/openapi.json
* http://localhost:8000/docs

## new_dataset cloud Function

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
--trigger-event-filters="bucket=$DATASET_BUCKET" \
--set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_NAME
```

## Key rings and keys

Explains how to create a KMS key on the command line for this project. 
See the following pages for the inspirations for this section:

* https://cloud.google.com/kms/docs/create-encryption-keys
* https://cloud.google.com/kms/docs/samples/kms-encrypt-symmetric#kms_encrypt_symmetric-python

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME

gcloud kms keyrings create "sds_keyring" --location "global"

gcloud kms keys create "unit_data_key" \
    --location "global" \
    --keyring "sds_keyring" \
    --purpose "encryption"
    
gcloud kms keys list --location "global" --keyring "sds_keyring"
```

To test the key works, do the following:

```bash
echo -n "Some text to be encrypted" > mysecret.txt
gcloud kms encrypt \
    --location "global" \
    --keyring "sds_keyring" \
    --key "unit_data_key" \
    --plaintext-file ./mysecret.txt \
    --ciphertext-file ./mysecret.txt.encrypted
gcloud kms decrypt \
    --location "global" \
    --keyring "sds_keyring" \
    --key "unit_data_key" \
    --ciphertext-file ./mysecret.txt.encrypted \
    --plaintext-file ./mysecret.txt.decrypted

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

export API_URL=https://sds-blahblah.a.run.app
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

### Running integration tests locally

This configuration makes use of the firestore and storage services running in Docker. The cloud function behaviour
is emulated by the test itself, or can be run manually by running the `SDX Simulate dataset publish` and `Cloud event trigger` http requests could in the thunderclient http collection in the devtools folder. 

```bash
docker-compose up

export FIRESTORE_EMULATOR_HOST=localhost:8200
export STORAGE_EMULATOR_HOST=http://localhost:9023
export SCHEMA_BUCKET_NAME=schema_bucket
export DATASET_BUCKET=dataset_bucket

export PYTHONPATH=../app
cd src/integration_tests
pytest integration_tests.py
```

# Contact

* mike.tidman@ons.gov.uk