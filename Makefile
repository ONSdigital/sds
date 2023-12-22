# Global Variables
AUTODELETE_DATASET_BUCKET_FILE=True
LOCAL_URL=http://localhost:3033
LOG_LEVEL=INFO
PUBLISH_DATASET_TOPIC_ID=ons-sds-publish-dataset
PUBLISH_SCHEMA_TOPIC_ID=ons-sds-publish-schema
PYTHONPATH=src/app
REGION=europe-west2
RETAIN_DATASET_FIRESTORE=True
SDS_APPLICATION_VERSION=development
SURVEY_MAP_URL=https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json
TEST_DATASET_PATH=src/test_data/json/
TEST_SCHEMA_PATH=src/test_data/json/

start-cloud-dev:
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=cloud-dev && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	source ./scripts/initialise_project.sh && \
	python -m uvicorn src.app.app:app --reload --port 3033

start-docker-dev:
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=docker-dev && \
	export DATASET_BUCKET_NAME=my-dataset-bucket && \
	export FIRESTORE_DB_NAME=mock-project-id-sds && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBSUB_EMULATOR_HOST=localhost:8085 && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SCHEMA_BUCKET_NAME=my-schema-bucket && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	python -m uvicorn src.app.app:app --reload --port 3033

lint-and-unit-test:
	black .
	isort . --profile black
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export FIRESTORE_DB_NAME=mock-project-id-sds && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	python -m pytest -vv --cov=src/app ./src/unit_tests/ -W ignore::DeprecationWarning
	python -m coverage report --omit="./src/app/repositories/*" --fail-under=90  -m

unit-test:
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export FIRESTORE_DB_NAME=mock-project-id-sds && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	python -m pytest -vv  --cov=src/app ./src/unit_tests/ -W ignore::DeprecationWarning
	python -m coverage report --omit="./src/app/repositories/*" --fail-under=90  -m

integration-test-local:
	export API_URL=${LOCAL_URL} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=int-test && \
	export DATASET_BUCKET_NAME=mock-project-id-sds-europe-west2-dataset && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	export GOOGLE_APPLICATION_CREDENTIALS=sandbox-token.json && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export OAUTH_CLIENT_ID=${LOCAL_URL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SCHEMA_BUCKET_NAME=mock-project-id-sds-europe-west2-schema && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	python -m pytest src/integration_tests -vv -W ignore::DeprecationWarning

integration-test-sandbox:
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=int-test && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	source ./scripts/initialise_project.sh && \
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
	export RETAIN_DATASET_FIRESTORE=${INT_RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL=${INT_LOG_LEVEL} && \
	export PROJECT_ID=${INT_PROJECT_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${INT_PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${INT_PUBLISH_DATASET_TOPIC_ID} && \
	export API_URL=${INT_API_URL} && \
	export OAUTH_CLIENT_ID=${INT_OAUTH_CLIENT_ID} && \
	export SURVEY_MAP_URL=${INT_SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME=${INT_FIRESTORE_DB_NAME} && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	python -m pytest src/integration_tests -vv -W ignore::DeprecationWarning

generate-spec:
	# export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	# export CONF=cloud-dev && \
	# export DATASET_BUCKET_NAME=my-schema-bucket && \
	# export FIRESTORE_DB_NAME=mock-project-id-sds && \
	# export LOCAL_URL=${LOCAL_URL} && \
	# export LOG_LEVEL=${LOG_LEVEL} && \
	# export PROJECT_ID=mock-project-id && \
	# export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	# export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	# export PYTHONPATH=${PYTHONPATH} && \
	# export REGION=${REGION} && \
	# export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	# export SCHEMA_BUCKET_NAME="the-bucket-name" && \
	# export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	# export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	python -m scripts.generate_openapi src.app.app:app --out gateway/openapi.yaml

lint:
	python -m black . --check
	python -m isort . --check-only --profile black
	python -m flake8 src --max-line-length=127

audit:
	python -m pip_audit

lint-fix:
	black .
	isort . --profile black

setup: requirements.txt
	pip install -r requirements.txt

initialise-project:
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	source ./scripts/initialise_project.sh

upload-schema:
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export CONF=int-test && \
	export LOCAL_URL=${LOCAL_URL} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PYTHONPATH=${PYTHONPATH} && \
	export REGION=${REGION} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	source ./scripts/initialise_project.sh && \
	python -m ./scripts/upload_schema.py
