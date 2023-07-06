from unittest import TestCase

from src.app.config.config_factory import config
from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    generate_headers,
    load_json,
    setup_session,
)
from src.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from src.test_data.shared_test_data import test_schema_subscriber_id


class E2ESchemaIntegrationTest(TestCase):
    def tearDown(self) -> None:
        cleanup()

    def setUp(self) -> None:
        cleanup()

    def test_schema_e2e(self):
        """
        Post a schema using the /schema api endpoint and check the metadata
        can be retrieved. Also check that schema can be retrieved directly from storage.
        """
        session = setup_session()
        headers = generate_headers()

        test_schema = load_json(config.TEST_SCHEMA_PATH)

        schema_post_response = session.post(
            f"{config.LOAD_BALANCER_ADDRESS}/v1/schema",
            json=test_schema,
            headers=headers,
        )
        print(schema_post_response.content)
        assert schema_post_response.status_code == 200
        assert "guid" in schema_post_response.json()

        received_messages = schema_pubsub_helper.pull_messages(
            test_schema_subscriber_id
        )

        received_messages_json = received_messages[0]
        assert received_messages_json == schema_post_response.json()

        test_schema_get_response = session.get(
            f"{config.LOAD_BALANCER_ADDRESS}/v1/schema_metadata?survey_id={test_schema['survey_id']}",
            headers=headers,
        )

        assert test_schema_get_response.status_code == 200

        response_as_json = test_schema_get_response.json()
        assert len(response_as_json) > 0

        for schema in response_as_json:
            assert schema == {
                "guid": schema["guid"],
                "survey_id": test_schema["survey_id"],
                "schema_location": f"{test_schema['survey_id']}/{schema['guid']}.json",
                "sds_schema_version": schema["sds_schema_version"],
                "sds_published_at": schema["sds_published_at"],
            }

            set_version_schema_response = session.get(
                f"{config.LOAD_BALANCER_ADDRESS}/v1/schema?"
                f"survey_id={schema['survey_id']}&version={schema['sds_schema_version']}",
                headers=headers,
            )

            assert set_version_schema_response.status_code == 200
            assert set_version_schema_response.json() == test_schema

            latest_version_schema_response = session.get(
                f"{config.LOAD_BALANCER_ADDRESS}/v1/schema?survey_id={schema['survey_id']}",
                headers=headers,
            )

            assert latest_version_schema_response.status_code == 200
            assert latest_version_schema_response.json() == test_schema
