# Global Variables
PYTHONPATH=app
TEST_DATASET_PATH=tests/test_data/json/
TEST_SCHEMA_PATH=tests/test_data/json/
GOOGLE_APPLICATION_CREDENTIALS=sandbox-key.json
AUTODELETE_DATASET_BUCKET_FILE=True
RETAIN_DATASET_FIRESTORE=True
LOG_LEVEL=INFO
PROJECT_ID = $(shell gcloud config get project)
OAUTH_BRAND_NAME = $(shell gcloud iap oauth-brands list --format='value(name)' --limit=1 --project=$(PROJECT_ID))
OAUTH_CLIENT_NAME = $(shell gcloud iap oauth-clients list $(OAUTH_BRAND_NAME) --format='value(name)' \
        --limit=1)
OAUTH_CLIENT_ID = $(shell echo $(OAUTH_CLIENT_NAME)| cut -d'/' -f 6)
LOCAL_URL=http://localhost:3033
SANDBOX_IP_ADDRESS = $(shell gcloud compute addresses list --global  --filter=name:$(PROJECT_ID)-sds-static-lb-ip --format='value(address)' --limit=1 --project=$(PROJECT_ID))
PUBLISH_SCHEMA_TOPIC_ID=ons-sds-publish-schema
PUBLISH_DATASET_TOPIC_ID=ons-sds-publish-dataset
PUBLISH_DATASET_ERROR_TOPIC_ID=ons-sds-publish-dataset-error
SURVEY_MAP_URL=https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json
SDS_APPLICATION_VERSION=development

start-cloud-dev:
	export CONF=cloud-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-schema && \
	export DATASET_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-dataset && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=${PROJECT_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME=${PROJECT_ID}-sds && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m uvicorn main:app --reload --port 3033

start-docker-dev:
	export CONF=docker-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	export PUBSUB_EMULATOR_HOST=localhost:8085 && \
	export DATASET_BUCKET_NAME=my-dataset-bucket && \
	export SCHEMA_BUCKET_NAME=my-schema-bucket && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME=${PROJECT_ID}-sds && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m uvicorn main:app --reload --port 3033

lint-and-unit-test:
	python -m ruff check .
	export PYTHONPATH=${PYTHONPATH} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME=${PROJECT_ID}-sds && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m pytest -vv --cov=app ./tests/unit_tests/ -W ignore::DeprecationWarning
	uv run python -m coverage report --omit="./app/repositories/*" --fail-under=90  -m

unit-test:
	export PYTHONPATH=${PYTHONPATH} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m pytest -vv  --cov=app ./tests/unit_tests/ -W ignore::DeprecationWarning
	uv run python -m coverage report --omit="./app/repositories/*" --fail-under=90  -m


integration-test-local:
	export CONF=int-test && \
	export PYTHONPATH=${PYTHONPATH} && \
    export DATASET_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-dataset && \
    export SCHEMA_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-schema && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export API_URL=${LOCAL_URL} && \
	export OAUTH_CLIENT_ID=${LOCAL_URL} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m pytest --order-scope=module tests/integration_tests -vv -W ignore::DeprecationWarning

integration-test-sandbox:
	export CONF=int-test && \
	export PYTHONPATH=${PYTHONPATH} && \
    export DATASET_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-dataset && \
    export SCHEMA_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-schema && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export PROJECT_ID=$(PROJECT_ID) && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export API_URL=https://${SANDBOX_IP_ADDRESS}.nip.io && \
	export OAUTH_CLIENT_ID=${OAUTH_CLIENT_ID} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME=${PROJECT_ID}-sds && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m pytest --order-scope=module tests/integration_tests -vv -W ignore::DeprecationWarning

#For use only by automated cloudbuild, is not intended to work locally.
integration-test-cloudbuild:
	export CONF=int-test-cloudbuild && \
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
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export API_URL=${INT_API_URL} && \
	export OAUTH_CLIENT_ID=${INT_OAUTH_CLIENT_ID} && \
	export SURVEY_MAP_URL=${INT_SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME=${INT_FIRESTORE_DB_NAME} && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m pytest --order-scope=module tests/integration_tests -vv -W ignore::DeprecationWarning

generate-spec:
	export CONF=cloud-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-schema && \
	export DATASET_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-dataset && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL=${LOG_LEVEL} && \
	export PROJECT_ID=${PROJECT_ID} && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export PUBLISH_DATASET_TOPIC_ID=${PUBLISH_DATASET_TOPIC_ID} && \
	export PUBLISH_DATASET_ERROR_TOPIC_ID=${PUBLISH_DATASET_ERROR_TOPIC_ID} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	export SDS_APPLICATION_VERSION=${SDS_APPLICATION_VERSION} && \
	uv run python -m scripts.generate_openapi app.main:app --out gateway/openapi.yaml

lint:
	uv run python -m ruff check .

audit:
	uv run python -m pip_audit

lint-fix:
	uv run python -m ruff check --fix .

setup:
	uv sync

.PHONY:  bump bump-patch bump-minor bump-major
bump:
	@echo "🔼 Bumping project version (patch)..."
	uv run --only-group version-check python .github/scripts/bump_version.py patch
	@echo "🔄 Generating new lock file..."
	uv lock

bump-patch:
	@echo "🔼 Bumping project version (patch)..."
	uv run --only-group version-check python .github/scripts/bump_version.py patch
	@echo "🔄 Generating new lock file..."
	uv lock

bump-minor:
	@echo "🔼 Bumping project version (minor)..."
	uv run --only-group version-check python .github/scripts/bump_version.py minor
	@echo "🔄 Generating new lock file..."
	uv lock

bump-major:
	@echo "🔼 Bumping project version (major)..."
	uv run --only-group version-check python .github/scripts/bump_version.py major
	@echo "🔄 Generating new lock file..."
	uv lock

