from unittest import TestCase
import pytest
from src.app.config.config_factory import config
from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    generate_headers,
    load_json,
    pubsub_setup,
    pubsub_teardown,
    setup_session,
    pubsub_purge_messages,
    inject_wait_time,
)
from src.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from src.test_data.schema_test_data import test_survey_id, test_survey_id_map
from src.test_data.shared_test_data import test_schema_subscriber_id


class E2ESchemaIntegrationTest(TestCase):
    schema_guid = None
    schema_metadatas = None
    test_schema = load_json(f"{config.TEST_SCHEMA_PATH}schema.json")
    session = None
    headers = None

    @classmethod
    def setup_class(self) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
        inject_wait_time(3) # Inject wait time to allow resources properly set up
        self.session = setup_session()
        self.headers = generate_headers()

    @classmethod
    def teardown_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed
        pubsub_purge_messages(schema_pubsub_helper, test_schema_subscriber_id)
        pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)

    @pytest.mark.order(1)
    def test_post_schema_v1(self):
        """
        Test the POST /v1/schema endpoint by publishing a schema and checking the response and the pub/sub message.
        """
        schema_post_response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=self.test_schema,
            headers=self.headers,
        )

        assert schema_post_response.status_code == 200
        assert "guid" in schema_post_response.json()
        self.schema_guid = schema_post_response.json()["guid"]

        received_messages = schema_pubsub_helper.pull_and_acknowledge_messages(
            test_schema_subscriber_id
        )

        # Retrieve and verify received messages from Pub/Sub
        received_messages_json = received_messages[0]
        assert received_messages_json == schema_post_response.json()


    @pytest.mark.order(2)
    def test_get_schema_metadata_v1(self):
        """
        Test the GET /v1/schema_metadata endpoint by retrieving the schema metadata and checking the response.
        """
        # Retrieve and verify schema metadata
        test_schema_get_response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata?survey_id={test_survey_id}",
            headers=self.headers,
        )

        assert test_schema_get_response.status_code == 200

        E2ESchemaIntegrationTest.schema_metadatas = test_schema_get_response.json()
        assert len(E2ESchemaIntegrationTest.schema_metadatas) > 0

        for schema_metadata in E2ESchemaIntegrationTest.schema_metadatas:
            assert schema_metadata == {
                "guid": schema_metadata["guid"],
                "survey_id": test_survey_id,
                "schema_location": f"{test_survey_id}/{schema_metadata['guid']}.json",
                "sds_schema_version": schema_metadata["sds_schema_version"],
                "sds_published_at": schema_metadata["sds_published_at"],
                "schema_version": self.test_schema["properties"]["schema_version"]["const"],
                "title": self.test_schema["title"],
            }


    @pytest.mark.order(3)
    def test_get_schema_v1(self):
        """
        Test the GET /v1/schema endpoint by retrieving the schema both by version and latest version and checking the response.
        """
        for schema_metadata in E2ESchemaIntegrationTest.schema_metadatas:
            # Verify schema retrieval by version
            set_version_schema_response = self.session.get(
                f"{config.API_URL}/v1/schema?"
                f"survey_id={schema_metadata['survey_id']}&version={schema_metadata['sds_schema_version']}",
                headers=self.headers,
            )

            assert set_version_schema_response.status_code == 200
            assert set_version_schema_response.json() == self.test_schema

            # Verify schema retrieval by the latest version
            latest_version_schema_response = self.session.get(
                f"{config.API_URL}/v1/schema?survey_id={schema_metadata['survey_id']}",
                headers=self.headers,
            )

            assert latest_version_schema_response.status_code == 200
            assert latest_version_schema_response.json() == self.test_schema


    @pytest.mark.order(4)
    def test_get_schema_v2(self):
        """
        Test the GET /v2/schema endpoint by retrieving the schema by GUID and checking the response.
        """
        for schema_metadata in E2ESchemaIntegrationTest.schema_metadatas:
            # Verify schema retrieval by GUID
            set_guid_schema_response = self.session.get(
                f"{config.API_URL}/v2/schema?guid={schema_metadata['guid']}",
                headers=self.headers,
            )

            assert set_guid_schema_response.status_code == 200
            assert set_guid_schema_response.json() == self.test_schema

    @pytest.mark.order(5)
    def test_survey_id_map(cls):
        """
        Retrieve survey mapping data using the /survey_list endpoint.
        Verify that the retrieved data matches the expected survey mapping data.
        """

        set_survey_id_map_response = cls.session.get(
            f"{config.API_URL}/v1/survey_list",
            headers=cls.headers,
        )

        assert set_survey_id_map_response.status_code == 200
        assert set_survey_id_map_response.json() == test_survey_id_map
