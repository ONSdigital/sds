start-cloud-dev:
	export CONF=cloud-dev && \
	export PYTHONPATH=src/app && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export DATASET_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-dataset-892a && \
	export GOOGLE_APPLICATION_CREDENTIALS=sandbox-key.json && \
	python -m uvicorn src.app.app:app --reload --port 3000


start-docker-dev:
	export CONF=docker-dev && \
	export PYTHONPATH=src/app && \
	export FIRESTORE_EMULATOR_HOST=localhost:8080 && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	export DATASET_BUCKET_NAME=bucket && \
	python -m uvicorn src.app.app:app --reload --port 3000


setup-localSDS-test:
	export CONF=IntegrationTestingLocalSDS && \
	export PYTHONPATH=src/app && \
	export SCHEMA_BUCKET_NAME=my-schema-bucket && \
	export DATASET_BUCKET_NAME=my-dataset-bucket && \
	export GOOGLE_APPLICATION_CREDENTIALS=dev-key.json && \
	pytest src/integration_tests/integration_tests.py -vv


setup-cloud-test:
	export CONF=IntegrationTestingCloud && \
	export PYTHONPATH=src/app && \
	export SCHEMA_BUCKET_NAME=ons-sds-sandbox-01-europe-west2-schema-892a && \
	export DATASET_BUCKET=ons-sds-sandbox-01-europe-west2-dataset-892a && \
	export GOOGLE_APPLICATION_CREDENTIALS=sandbox-key.json && \
	pytest src/integration_tests/integration_tests.py -vv

setup-docker-test:
	export CONF=IntegrationTestingDocker && \
	export PYTHONPATH=src/app && \
	export SCHEMA_BUCKET_NAME=my-schema-bucket && \
	export DATASET_BUCKET_NAME=my-dataset-bucket && \
	export FIRESTORE_EMULATOR_HOST=localhost:8200 && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	pytest src/integration_tests/integration_tests.py -vv

unit-test:
	export PYTHONPATH=src/app && \
	export CONF=unit && \
	export DATASET_BUCKET_NAME=my-schema-bucket && \
	export TEST_DATASET_PATH=src/test_data/dataset.json && \
	export TEST_SCHEMA_PATH=src/test_data/schema.json && \
	export STORAGE_EMULATOR_HOST=http://localhost:9023 && \
	pytest --cov=src/app ./src/unit_tests/
	coverage report --fail-under=90 -m

lint:
	black . --check
	isort . --check-only --profile black
	flake8 src --max-line-length=127

lint-fix:
	black .
	isort . --profile black

setup: requirements.txt
	pip install -r requirements.txt