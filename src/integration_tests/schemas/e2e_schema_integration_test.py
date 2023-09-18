from unittest import TestCase

from src.app.config.config_factory import config
from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    generate_headers,
    load_json,
    pubsub_setup,
    pubsub_teardown,
    setup_session,
)
from src.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from src.test_data.schema_test_data import test_list_survey_id, test_survey_id
from src.test_data.shared_test_data import test_schema_subscriber_id


class E2ESchemaIntegrationTest(TestCase):
    def setUp(self) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)

    def tearDown(self) -> None:
        cleanup()
        pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)

    def test_schema_e2e(self):
        """
        Post a schema using the /schema api endpoint and check the metadata
        can be retrieved. Also check that schema can be retrieved directly from storage.
        """
        session = setup_session()
        headers = generate_headers()

        test_schema = load_json(config.TEST_SCHEMA_PATH)

        schema_post_response = session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=test_schema,
            headers=headers,
        )

        assert schema_post_response.status_code == 200
        assert "guid" in schema_post_response.json()

        received_messages = schema_pubsub_helper.pull_and_acknowledge_messages(
            test_schema_subscriber_id
        )

        received_messages_json = received_messages[0]
        assert received_messages_json == schema_post_response.json()

        test_schema_get_response = session.get(
            f"{config.API_URL}/v1/schema_metadata?survey_id={test_survey_id}",
            headers=headers,
        )

        assert test_schema_get_response.status_code == 200

        response_as_json = test_schema_get_response.json()
        assert len(response_as_json) > 0

        for schema in response_as_json:
            assert schema == {
                "guid": schema["guid"],
                "survey_id": test_survey_id,
                "schema_location": f"{test_survey_id}/{schema['guid']}.json",
                "sds_schema_version": schema["sds_schema_version"],
                "sds_published_at": schema["sds_published_at"],
                "schema_version": test_schema["properties"]["schema_version"]["const"],
            }

            set_version_schema_response = session.get(
                f"{config.API_URL}/v1/schema?"
                f"survey_id={schema['survey_id']}&version={schema['sds_schema_version']}",
                headers=headers,
            )

            assert set_version_schema_response.status_code == 200
            assert set_version_schema_response.json() == test_schema

            latest_version_schema_response = session.get(
                f"{config.API_URL}/v1/schema?survey_id={schema['survey_id']}",
                headers=headers,
            )

            assert latest_version_schema_response.status_code == 200
            assert latest_version_schema_response.json() == test_schema

            set_guid_schema_response = session.get(
                f"{config.API_URL}/v2/schema?guid={schema['guid']}",
                headers=headers,
            )

            assert set_guid_schema_response.status_code == 200
            assert set_guid_schema_response.json() == test_schema


def test_list_unique_survey_id(self):
    """
    Post schemas using the /schema api endpoint with multiple survey IDs and check that the /survey_list endpoint returns
    the list of unique survey IDs.
    """
    session = setup_session()
    headers = generate_headers()

    test_schema = load_json(config.TEST_SCHEMA_PATH)

    schema_post_response = session.post(
        f"{config.API_URL}/v1/schema?survey_id={test_list_survey_id[0]}",
        json=test_schema,
        headers=headers,
    )

    assert schema_post_response.status_code == 200

    for survey_id in test_list_survey_id:
        schema_post_response = session.post(
            f"{config.API_URL}/v1/schema?survey_id={survey_id}",
            json=test_schema,
            headers=headers,
        )
        assert schema_post_response.status_code == 200

    set_list_unique_survey_id_response = session.get(
        f"{config.API_URL}/v1/survey_list",
        headers=headers,
    )

    assert set_list_unique_survey_id_response.status_code == 200
    assert set_list_unique_survey_id_response.json() == test_list_survey_id
