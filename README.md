# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

- https://confluence.ons.gov.uk/display/SDC/SDS

---

## Dockerized

The docker-compose will launch the SDS application, two storage emulators(firebase and bucket), the new_dataset cloud function and a supporting publish dataset endpoint. The SDS application will also support hot reloading within the `/src/app` directory.

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
  "title": "Which side was better?",
  "schema_version": "v1.0.0",
  "data": [
    {
      "ruref": "43532",
      "unit_data": 
        {
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
    }
 ]
}'
```

---

## Running locally

To run this service locally, you will need the following:

- Python 3.11
- Docker or credentials for GCloud

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
use of the sandbox project. Instructions for setting this up are included in the IaC repo.
You will need to take note of the schema and dataset bucket names for the project you are using.

Once you have setup your project, you will need a key file to allow SDS to talk to bucket storage
and the database. To create one:

- Go the IAM page and select Service accounts
- Create a new service account
- Call it "test"
- Add the roles that are needed for testing
- Go into service account and create a key. This will download a JSON file to your machine
- Copy the downloaded JSON file to this directory and rename to `key.json`

To run SDS locally, activate the virtual environment, then run the following commands (ensuring that the values in the
makefile represent the connections you wish to make):

```bash
make start-cloud-dev
```

### Running the SDS with service emulators

The Firestore and Cloud Storage emulators run in Docker. To connect to the Firestore emulator running locally in Docker,
run the following commands:

```bash
docker-compose up
docker-compose stop api

make start-docker-dev
```

## Running linting and unit tests

As part of the CI pipeline we ensure the code is linted and tested. To run the linting run: 

```bash
make lint
```

To automatically fix any linting issues run:

```bash
make lint-fix
```

To run the unit tests run:

```bash
make unit-test
```

## OpenAPI Specification

As this runs in FastAPI, the Open API Spec and interactive API docs are auto-generated from the Python code and
can be reached by going to the following URLs (once running):

- http://localhost:8000/openapi.json
- http://localhost:8000/docs

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
--set-env-vars="DATASET_BUCKET_NAME=$DATASET_BUCKET,SCHEMA_BUCKET_NAME=$SCHEMA_BUCKET_NAME,CONF=cloud-build,AUTODELETE_DATASET_BUCKET_FILE=True,LOG_LEVEL=DEBUG,PROJECT_ID=$PROJECT_NAME,SCHEMA_TOPIC_ID=ons-sds-schema-events,DATASET_TOPIC_ID=ons-sds-dataset-events"
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
 
make cloud-test
```

### SDS API service is local

This configuration allows you to debug the SDS API locally but talk to real Google services. Run them like this
(replacing `my-schema-bucket` with the real schema bucket and `a-place-for-datasets` with the real dataset bucket):

```bash
gcloud auth login
gcloud config set project $PROJECT_NAME

make localSDS-test
```

### Running integration tests locally

This configuration makes use of the firestore and storage services running in Docker. The cloud function behaviour
is emulated by the test itself, or can be run manually by running the `SDX Simulate dataset publish` and `Cloud event trigger` http requests could in the thunderclient http collection in the devtools folder.

```bash
docker-compose up

make docker-test
```

# Contact

- mike.tidman@ons.gov.uk
