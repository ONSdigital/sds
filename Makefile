# Global Variables
PYTHONPATH=app
AUTODELETE_DATASET_BUCKET_FILE=True
RETAIN_DATASET_FIRESTORE=True
LOG_LEVEL=INFO
PROJECT_ID = $(shell gcloud config get project)
LOCAL_URL=http://localhost:3033
SANDBOX_IP_ADDRESS = $(shell gcloud compute addresses list --global  --filter=name:$(PROJECT_ID)-sds-static-lb-ip --format='value(address)' --limit=1 --project=$(PROJECT_ID))
PUBLISH_SCHEMA_TOPIC_ID=ons-sds-publish-schema

# Please run gcloud auth application-default login before running the following commands that interact with GCP services
start-cloud-dev:
	export SCHEMA_BUCKET_NAME='${PROJECT_ID}-sds-europe-west2-schema' && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export LOG_LEVEL='DEBUG' && \
	export PROJECT_ID=${PROJECT_ID} && \
	export FIRESTORE_DB_NAME=''${PROJECT_ID}-sds'' && \
	uv run python -m uvicorn app.main:app --reload --port 3033

lint-and-unit-tests:
	uv run python -m ruff check .
	export CONF='unit' && \
	export SCHEMA_BUCKET_NAME="the-sds-schema-bucket" && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	uv run python -m pytest -vv  --cov=app ./tests/unit_tests/ -W ignore::DeprecationWarning
	uv run python -m coverage report --omit="./app/repositories/*" --fail-under=90  -m

unit-tests:
	export CONF='unit' && \
	export SCHEMA_BUCKET_NAME="the-sds-schema-bucket" && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	uv run python -m pytest -vv  --cov=app ./tests/unit_tests/ -W ignore::DeprecationWarning
	uv run python -m coverage report --omit="./app/repositories/*" --fail-under=90  -m

# Spinning up emulators in docker is required to run the local integration tests.
integration-test-local:
	export CONF='local-int-tests' && \
	export PROJECT_ID='emulated-project-id' && \
	export SCHEMA_BUCKET_NAME='emulated-schema-bucket' && \
	export PYTHONPATH=${PYTHONPATH} && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export AUTODELETE_DATASET_BUCKET_FILE=${AUTODELETE_DATASET_BUCKET_FILE} && \
	export RETAIN_DATASET_FIRESTORE=${RETAIN_DATASET_FIRESTORE} && \
	export PUBLISH_SCHEMA_TOPIC_ID='emulated-sds-schema-topic' && \
	export API_URL=${LOCAL_URL} && \
	export SURVEY_MAP_URL=${SURVEY_MAP_URL} && \
	export FIRESTORE_DB_NAME="sds-firestore" && \
	uv run python -m pytest --order-scope=module tests/integration_tests -vv -W ignore::DeprecationWarning

# Please run gcloud auth application-default login before running the following commands that interact with GCP services
integration-test-sandbox:
	export CONF='sandbox-int-tests' && \
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
	export CONF='cloudbuild-int-tests' && \
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
	export PYTHONPATH=. && \
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
	uv run python .github/scripts/generate_openapi.py app.main:app --out gateway/openapi.yaml

lint:
	uv run python -m ruff check .

audit:
	uv run python -m pip_audit

lint-fix:
	uv run python -m ruff check --fix .

setup:
	@command -v uv >/dev/null 2>&1 || { \
		echo "uv not found – installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
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

