# Global Variables
PYTHONPATH=src/app
TEST_DATASET_PATH=src/test_data/dataset.json
TEST_SCHEMA_PATH=src/test_data/schema.json
GOOGLE_APPLICATION_CREDENTIALS=sandbox-key.json

start-cloud-dev:
	export CONF=cloud-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	python -m uvicorn src.app.app:app --reload --port 3000


start-docker-dev:
	export CONF=docker-dev && \
	export PYTHONPATH=${PYTHONPATH} && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	export DATASET_BUCKET_NAME=bucket && \
	python -m uvicorn src.app.app:app --reload --port 3000


localSDS-test:
	export CONF=int-test-localSDS && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	python -m pytest src/integration_tests/integration_tests.py -vv


cloud-test:
	export CONF=cloud-int-test-local && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} && \
	export API_URL=https://sds-jjpah7fbzq-nw.a.run.app && \
	python -m pytest src/integration_tests/integration_tests.py -vv


docker-test:
	export CONF=int-test-docker && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=my-schema-bucket && \
	export DATASET_BUCKET_NAME=my-dataset-bucket && \
	export FIRESTORE_EMULATOR_HOST=localhost:8200 && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	python -m pytest src/integration_tests/integration_tests.py -vv


unit-test:
	export PYTHONPATH=${PYTHONPATH} && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export SCHEMA_BUCKET_NAME="the bucket name" && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	python -m pytest --cov=src/app ./src/unit_tests/
	python -m coverage report --fail-under=90 -m


cloud-int-test:
	export CONF=cloud-int-test-remote && \
	export PYTHONPATH=${PYTHONPATH} && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export TEST_DATASET_PATH=${TEST_DATASET_PATH} && \
	export TEST_SCHEMA_PATH=${TEST_SCHEMA_PATH} && \
	export ACCESS_TOKEN=${ACCESS_TOKEN} && \
	export API_URL=${API_URL} && \
	export DATASET_BUCKET_NAME=${DATASET_BUCKET_NAME} && \
	python -m pytest src/integration_tests/integration_tests.py -vv


lint:
	black . --check
	isort . --check-only --profile black
	flake8 src --max-line-length=127


lint-fix:
	black .
	isort . --profile black


setup: requirements.txt
	pip install -r requirements.txt