import pytest

from app.config import settings
from tests.integration_tests.helpers.integration_helpers import load_json
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_data.shared_test_data import test_survey_id_list


@pytest.fixture
def test_schema_list():
    schema_list: list[dict] = []
    schema_list.append(load_json(f"{settings.TEST_SCHEMA_PATH}schema_2.json"))
    schema_list.append(load_json(f"{settings.TEST_SCHEMA_PATH}schema.json"))

    yield schema_list

@pytest.fixture
def post_schema(test_schema_list):
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