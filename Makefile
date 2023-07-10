# Global Variables
PYTHONPATH=src/app
TEST_DATASET_PATH=src/test_data/dataset.json
TEST_SCHEMA_PATH=src/test_data/schema.json
GOOGLE_APPLICATION_CREDENTIALS=sandbox-key.json
AUTODELETE_DATASET_BUCKET_FILE=True
LOG_LEVEL=INFO
PROJECT_ID = $(shell gcloud config get project)
OAUTH_BRAND_NAME = $(shell gcloud iap oauth-brands list --format='value(name)' --limit=1 --project=$(PROJECT_ID))
OAUTH_CLIENT_NAME = $(shell gcloud iap oauth-clients list $(OAUTH_BRAND_NAME) --format='value(name)' \
        --limit=1)
OAUTH_CLIENT_ID = $(shell echo $(OAUTH_CLIENT_NAME)| cut -d'/' -f 6)
LOCAL_URL:=http://localhost:3000
PUBLISH_SCHEMA_TOPIC_ID=ons-sds-publish-schema
PUBLISH_DATASET_TOPIC_ID=ons-sds-publish-dataset

start-cloud-dev:
	export CONF=cloud-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=${PROJECT_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	python -m uvicorn src.app.app:app --reload --port 3000


start-docker-dev:
	export CONF=docker-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	export DATASET_BUCKET_NAME=my-dataset-bucket && \
	export SCHEMA_BUCKET_NAME=my-schema-bucket && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	python -m uvicorn src.app.app:app --reload --port 3000

lint-and-unit-test:
	black .
	isort . --profile black
	export PYTHONPATH=${PYTHONPATH} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	python -m pytest -vv --cov=src/app ./src/unit_tests/ -W ignore::DeprecationWarning
	python -m coverage report --omit="./src/app/repositories/*" --fail-under=90  -m

unit-test:
	export PYTHONPATH=${PYTHONPATH} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	python -m pytest -vv  --cov=src/app ./src/unit_tests/ -W ignore::DeprecationWarning
	python -m coverage report --omit="./src/app/repositories/*" --fail-under=90  -m


integration-test-local:
	export CONF=int-test && \
	export PYTHONPATH=${PYTHONPATH} && \
    export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
    export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export API_URL=${LOCAL_URL} && \
	export OAUTH_CLIENT_ID=${LOCAL_URL} && \
	python -m pytest src/integration_tests -vv -W ignore::DeprecationWarning

integration-test-sandbox:
	export CONF=int-test && \
	export PYTHONPATH=${PYTHONPATH} && \
    export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
    export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export PROJECT_ID=$(PROJECT_ID) && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export API_URL=https://34.36.238.222.nip.io && \
	export OAUTH_CLIENT_ID=${OAUTH_CLIENT_ID} && \
	python -m pytest src/integration_tests -vv -W ignore::DeprecationWarning

#For use only by automated cloudbuild, is not intended to work locally. 
integration-test-cloudbuild:
	export CONF=int-test-cloudbuild && \
	export PYTHONPATH=${PYTHONPATH} && \
    export DATASET_BUCKET_NAME=${INT_DATASET_BUCKET_NAME} && \
    export SCHEMA_BUCKET_NAME=${INT_SCHEMA_BUCKET_NAME} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${INT_AUTODELETE_DATASET_BUCKET_FILE} && \
	export LOG_LEVEL=${INT_LOG_LEVEL} && \
	export PROJECT_ID=${INT_PROJECT_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${INT_PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${INT_PUBLISH_DATASET_TOPIC_ID} && \
	export API_URL=${INT_API_URL} && \
	export OAUTH_CLIENT_ID=${INT_OAUTH_CLIENT_ID} && \
	python -m pytest src/integration_tests -vv -W ignore::DeprecationWarning

lint:
	black . --check
	isort . --check-only --profile black
	flake8 src --max-line-length=127

audit:
	python -m pip_audit

lint-fix:
	black .
	isort . --profile black


setup: requirements.txt
	pip install -r requirements.txt