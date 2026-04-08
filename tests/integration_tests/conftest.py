import pytest
from google.cloud import firestore
from sds_common.test_helpers.integration_helpers import pubsub_setup, inject_wait_time, pubsub_teardown

from app.config import settings
from app.models.dataset_models import DatasetMetadata
from tests.integration_tests.helpers.firestore_helpers import upload_dataset
from tests.integration_tests.helpers.integration_helpers import load_json, cleanup
from tests.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_data.dataset_test_data import dataset_metadata_collection_for_endpoints_test, \
    dataset_unit_data_collection_for_endpoints_test
from tests.test_data.shared_test_data import test_survey_id_list, test_schema_subscriber_id


@pytest.fixture
def test_schema_list():
    schema_list: list[dict] = [load_json(f"{settings.TEST_SCHEMA_PATH}schema_2.json"),
                               load_json(f"{settings.TEST_SCHEMA_PATH}schema.json")]

    yield schema_list


@pytest.fixture
def setup_schema(test_schema_list):
    cleanup()

    for survey_id in test_survey_id_list:
        make_iap_request(
            "POST",
            f"/v1/schema?survey_id={survey_id}",
            json=test_schema_list[1]
        )

        make_iap_request(
            "POST",
            f"/v1/schema?survey_id={survey_id}",
            json=test_schema_list[0]
        )

    yield True

    cleanup()


@pytest.fixture
def setup_post_schema():
    cleanup()
    pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
    if not settings.API_URL.__contains__("local"):
        inject_wait_time(3) # Inject wait time to allow resources properly set up

    yield True

    pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)
    cleanup()


@pytest.fixture
def setup_dataset():
    cleanup()

    firestore_client = firestore.Client(project=settings.PROJECT_ID, database=settings.FIRESTORE_DB_NAME)
    dataset_metadata: list[DatasetMetadata] = upload_dataset(
        firestore_client,
        dataset_metadata_collection_for_endpoints_test,
        dataset_unit_data_collection_for_endpoints_test
    )

    yield dataset_metadata

    cleanup()
