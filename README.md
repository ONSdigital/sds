# Supplementary Data Service (sds)

More information on this service can be found on Confluence:

- https://confluence.ons.gov.uk/display/SDC/SDS

## Dockerized

The docker-compose will launch the SDS application, two storage emulators(firebase and bucket), the new_dataset cloud function and a supporting publish dataset endpoint. The SDS application will also support hot reloading within the `/src/app` directory.

```
docker-compose up
```

Once, loaded you can do the following:

- View the API service docs [localhost:3033/docs](http://localhost:3033/docs).
- See files put into cloud storage within `devtools/gcp-storage-emulator/data/default-bucket`.
- Utilize the firestore emulator [localhost:4001/firestore](http://localhost:4001/firestore).
- Simulate the SDX publish process, invoked with a dataset as follows.

```
curl -X POST localhost:3006 \
-H "Content-Type: application/cloudevents+json" \
-d '{ "survey_id": "NRX",
  "period_id": "ttt",
  "title": "Which side was better?",
  "schema_version": "v1.0.0",
  "form_types": [
    "klk",
    "xyz",
    "tzr"
  ],
  "data": [
    {
      "identifier": "43532",
      "unit_data":
        {
        "runame": "Pipes and Maps Ltd",
        "local_unit": [
            {
                "identifier": "2012763A",
                "luname": "Maps Factory"
            },
            {
                "identifier": "20127364B",
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
Missing infrastructure for local docker

Topic for publisher_service.py and call on init
```python
    def create_topic(self, topic_id) -> None:
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        topic = self.publisher.create_topic(request={"name": topic_path})
```
Add the following topic and subscription and call it (before its used)
```python
    def create_topic() -> None:
        topic_path = subscriber.topic_path(
        config.PROJECT_ID, config.COLLECTION_EXERCISE_END_TOPIC_ID
        )
        topic = publisher.create_topic(request={"name": topic_path})
```

```python
    from google.cloud import pubsub_v1

    base_url = "depends on if you are wanting to use GCP or local"
    endpoint = "/collection-exercise-end"
    
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(config.PROJECT_ID, config.COLLECTION_EXERCISE_END_TOPIC_ID)
    subscription_path = subscriber.subscription_path(config.PROJECT_ID, config.COLLECTION_EXERCISE_END_SUBSCRIPTION_ID)
    
    push_config = pubsub_v1.types.PushConfig(push_endpoint=base_url+endpoint)
    
    
    def create_subscription() -> None:
        with subscriber:
            subscription = subscriber.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                    "push_config": push_config,
                }
            )
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

## Setting up GPG Key

- For signing commits to the git repository, create a new GPG key if you don't have an existing key. Follow the [link](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key) for creating a new GPG Key
- For the adding the new key to the account, follow the [link](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account)
- For telling Git about the Signing Key(Only needed once),follow the [link](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key)

## OpenAPI Specification

The openapi spec file in gateway/openapi.yaml should not be edited manually as it can be autogenerated using FastAPI utilities. This file should be regenerated every time the app changes. To autogenerate the file run make generate-spec.

## new_dataset cloud Function

`new_dataset` runs as a Cloud Function. It is Triggered by uploading a new dataset file to the dataset storage bucket.
To deploy the Cloud Function, run the following locally, but set the PROJECT_NAME environment variables first:

```bash
PROJECT_NAME=ons-sds-sandbox-01
gcloud auth login
gcloud config set project $PROJECT_NAME

cd src/app/
gcloud functions deploy new-dataset-function \
--no-allow-unauthenticated \
--gen2 \
--ingress-settings=all \
--runtime=python311 \
--region=europe-west2 \
--source=. \
--entry-point=new_dataset \
--timeout=3600s \
--memory=512MiB \
--cpu=1 \
--trigger-http \
--set-env-vars="DATASET_BUCKET_NAME=$PROJECT_NAME-sds-europe-west2-dataset,SCHEMA_BUCKET_NAME=$PROJECT_NAME-sds-europe-west2-schema,CONF=cloud-build,AUTODELETE_DATASET_BUCKET_FILE=True,RETAIN_DATASET_FIRESTORE=True,LOG_LEVEL=DEBUG,PROJECT_ID=$PROJECT_NAME,FIRESTORE_DB_NAME=$PROJECT_NAME-sds,PUBLISH_SCHEMA_TOPIC_ID=ons-sds-publish-schema,PUBLISH_DATASET_TOPIC_ID=ons-sds-publish-dataset,PUBLISH_DATASET_ERROR_TOPIC_ID=ons-sds-publish-dataset-error,SURVEY_MAP_URL=https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json,SDS_APPLICATION_VERSION=development"
```

## Running the integration tests

The integration tests will work in a number of different ways depending on how you want to test the SDS API service
and SDS cloud function. The following sections describe a number of combinations

### Everything running in the cloud

In this configuration, the integration test uses the SDS API service running in Cloud Run and the new-dataset-function
on Cloud Functions of your test/dev GCP project. Please note that the SDS and cloud function are not the updated version unless
run after creating a PR and gone through the pipeline. These services both talk to Firestore and Cloud Storage running on the same project.
This test configuration is also what is run at the end of the Cloud Build deployment.

```bash
PROJECT_NAME=ons-sds-sandbox-01
gcloud auth login
gcloud config set project $PROJECT_NAME

make integration-test-sandbox
```

### Running integration tests locally

This configuration makes use of the firestore and storage services running in Docker. The cloud function behaviour
is emulated by the test itself, or can be run manually by running the `SDX Simulate dataset publish` and `Cloud event trigger` http requests could in the thunderclient http collection in the devtools folder.

```bash
docker-compose up

make integration-test-local
```

# Contact

- [sds.cir.team@ons.gov.uk](mailto:sds.cir.team@ons.gov.uk)
