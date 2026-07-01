# Global Variables
PYTHONPATH=app
PROJECT_ID = $(shell gcloud config get project)
LOCAL_URL=localhost:3033
SANDBOX_IP_ADDRESS = $(shell gcloud compute addresses list --global  --filter=name:$(PROJECT_ID)-sds-static-lb-ip --format='value(address)' --limit=1 --project=$(PROJECT_ID))

# Please run gcloud auth application-default login before running the following commands that interact with GCP services
start-cloud-dev:
	export LOG_LEVEL='DEBUG' && \
	export PROJECT_ID=${PROJECT_ID} && \
	export FIRESTORE_DB_NAME='${PROJECT_ID}-sds' && \
	uv run python -m uvicorn app.main:app --reload --port 3033

lint-and-unit-tests:
	uv run python -m ruff check .
	export CONF='unit' && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	uv run python -m pytest -vv  --cov=app ./tests/unit_tests/ -W ignore::DeprecationWarning
	uv run python -m coverage report --omit="./app/repositories/*" --fail-under=90  -m

unit-tests:
	export CONF='unit' && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	uv run python -m pytest --cov=app --cov-fail-under=90 --cov-report term-missing --cov-config=.coveragerc_unit -vv ./tests/unit_tests/ -W ignore::DeprecationWarning
	make unit-tests-deprecated

unit-tests-deprecated:
	export CONF='unit' && \
	export PROJECT_ID=mock-project-id && \
	export PUBLISH_SCHEMA_TOPIC_ID=${PUBLISH_SCHEMA_TOPIC_ID} && \
	export FIRESTORE_DB_NAME="the-firestore-db-name" && \
	export ENDPOINTS_DEPRECATED="true" && \
	uv run python -m pytest --cov=app --cov-fail-under=90 --cov-report term-missing --cov-config=.coveragerc_unit_deprecated -vv ./tests/unit_tests/ -W ignore::DeprecationWarning

# Spinning up emulators in docker is required to run the local integration tests.
integration-tests-local:
	export CONF='local-int-tests' && \
	export PROJECT_ID='mock-project-id' && \
	export PYTHONPATH=${PYTHONPATH} && \
	export PUBLISH_SCHEMA_TOPIC_ID='emulated-sds-schema-topic' && \
	export API_URL=${LOCAL_URL} && \
	export URL_SCHEME='http' && \
	export PUBSUB_EMULATOR_HOST=localhost:8085 && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
	uv run python -m pytest --order-scope=module tests/integration_tests -vv -W ignore::DeprecationWarning

# Please run gcloud auth application-default login before running the following commands that interact with GCP services
# Please ensure user account has role Service Account Token Creator
integration-tests-sandbox:
	export CONF='sandbox-int-tests' && \
	export PYTHONPATH=${PYTHONPATH} && \
	export PROJECT_ID=${PROJECT_ID} && \
	export API_URL='${SANDBOX_IP_ADDRESS}.nip.io' && \
	export FIRESTORE_DB_NAME='${PROJECT_ID}-sds' && \
	export URL_SCHEME='https' && \
	export SECRET_ID='iap-secret' && \
	uv run python -m pytest --order-scope=module tests/integration_tests -vv -W ignore::DeprecationWarning

# Spinning up emulators in docker is required to run this command successfully.
generate-spec:
	export PYTHONPATH=. && \
	export PROJECT_ID='mock-project-id' && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
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

