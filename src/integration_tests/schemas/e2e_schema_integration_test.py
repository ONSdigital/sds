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
from src.test_data.schema_test_data import test_survey_id_map
from src.test_data.shared_test_data import test_schema_subscriber_id, test_survey_id_list, test_survey_id


class E2ESchemaIntegrationTest(TestCase):
    test_schema = None
    session = None
    headers = None
    schema_metadatas_dict = None

    @classmethod
    def setup_class(self) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
        inject_wait_time(3) # Inject wait time to allow resources properly set up
        # initialise class attributes
        self.session = setup_session()
        self.headers = generate_headers()
        self.test_schema = load_json(f"{config.TEST_SCHEMA_PATH}schema.json")
        self.schema_metadatas_dict = {}

    @classmethod
    def teardown_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed
        pubsub_purge_messages(schema_pubsub_helper, test_schema_subscriber_id)
        pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)

    @pytest.mark.order(1)
    def test_post_schema_v1(self):
        """
        Test the POST /v1/schema endpoint by publishing schemas from test_survey_id_list and checking the response and the pub/sub message.

        * We post a schema for each survey_id in survey_id_list and check the response
        * We retrieve and verify received messages from Pub/Sub
        """
        for survey_id in test_survey_id_list:

            schema_post_response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={survey_id}",
            json=self.test_schema,
            headers=self.headers,
            )

            assert schema_post_response.status_code == 200
            assert "guid" in schema_post_response.json()

            received_messages = schema_pubsub_helper.pull_and_acknowledge_messages(
                test_schema_subscriber_id
            )

            # Retrieve and verify received messages from Pub/Sub
            received_messages_json = received_messages[0]
            assert received_messages_json == schema_post_response.json()


    @pytest.mark.order(2)
    def test_get_schema_metadata_v1(self):
        """
        Test the GET /v1/schema_metadata endpoint by retrieving the schema metadata for each test_survey_id and checking the response.

        * We retrieve and verify schema metadata
        """

        for survey_id in test_survey_id_list:
            if survey_id in E2ESchemaIntegrationTest.schema_metadatas_dict:
                continue # Skip if schema metadata already retrieved
            schema_metadata_response = self.session.get(
                f"{config.API_URL}/v1/schema_metadata?survey_id={survey_id}",
                headers=self.headers,
            )
            assert schema_metadata_response.status_code == 200
            # Add json to dict with survey_id as key
            E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id] = schema_metadata_response.json()
            assert len(E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id]) > 0
        
            for schema_metadata in E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id]:
                assert schema_metadata == {
                    "guid": schema_metadata["guid"],
                    "survey_id": survey_id,
                    "schema_location": f"{survey_id}/{schema_metadata['guid']}.json",
                    "sds_schema_version": schema_metadata["sds_schema_version"],
                    "sds_published_at": schema_metadata["sds_published_at"],
                    "schema_version": self.test_schema["properties"]["schema_version"]["const"],
                    "title": self.test_schema["title"],
                }

    @pytest.mark.order(3)
    def test_get_schema_v1(self):
        """
        Test the GET /v1/schema endpoint by retrieving the schema both by version and latest version and checking the response.

        * We retrieve the schema by version and check the response
        """
        for survey_id in test_survey_id_list:
            for schema_metadata in E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id]:
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
                
                number_of_versions = test_survey_id_list.count(survey_id)
                if survey_id == test_survey_id:
                    assert latest_version_schema_response.json().get("sds_schema_version") == number_of_versions # Check if the returned sds_schema_version matches the number of schemas posted (i.e. latest version)


    @pytest.mark.order(4)
    def test_get_schema_v2(self):
        """
        Test the GET /v2/schema endpoint by retrieving the schema by GUID and checking the response.

        * We retrieve the schema by GUID and check the response
        """
        for survey_id in test_survey_id_list:
            for schema_metadata in E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id]:
                # Verify schema retrieval by GUID
                set_guid_schema_response = self.session.get(
                    f"{config.API_URL}/v2/schema?guid={schema_metadata['guid']}",
                    headers=self.headers,
                )

                assert set_guid_schema_response.status_code == 200
                assert set_guid_schema_response.json() == self.test_schema

    @pytest.mark.order(5)
    def test_survey_id_map(self):
        """
        Retrieve survey mapping data using the /survey_list endpoint.
        Verify that the retrieved data matches the expected survey mapping data.

        * We retrieve the survey mapping data and check the response
        """

        set_survey_id_map_response = self.session.get(
            f"{config.API_URL}/v1/survey_list",
            headers=self.headers,
        )

        assert set_survey_id_map_response.status_code == 200
        assert set_survey_id_map_response.json() == test_survey_id_map
