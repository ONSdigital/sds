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
    is_json_response,
)
from src.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from src.test_data.schema_test_data import test_survey_id_map
from src.test_data.shared_test_data import test_schema_subscriber_id, test_survey_id_list
from src.test_data.schema_test_data import invalid_survey_id, invalid_data, test_survey_id

class E2ESchemaIntegrationTest(TestCase):
    session = None
    headers = None
    test_schemas = None
    schema_metadatas_dict = None

    @classmethod
    def setup_class(self) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
        inject_wait_time(3) # Inject wait time to allow resources properly set up
        # initialise class attributes
        self.session = setup_session()
        self.headers = generate_headers()
        self.test_schemas = []
        # We add the 2nd version of the schema first to ease the testing of the schema as metadata endpoint lists newest schema versions first
        self.test_schemas.append(load_json(f"{config.TEST_SCHEMA_PATH}schema_2.json"))
        self.test_schemas.append(load_json(f"{config.TEST_SCHEMA_PATH}schema.json"))
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
        # Post v1 schema for each survey_id - v1 is stored in the second index of the test_schemas list
        for survey_id in test_survey_id_list:

            schema_post_response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={survey_id}",
            json=self.test_schemas[1],
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

        # Post v2 schema for each survey_id - v2 is stored in the first index of the test_schemas list
        for survey_id in test_survey_id_list:

            schema_post_response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={survey_id}",
            json=self.test_schemas[0],
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
            schema_metadata_response = self.session.get(
                f"{config.API_URL}/v1/schema_metadata?survey_id={survey_id}",
                headers=self.headers,
            )
            assert schema_metadata_response.status_code == 200
            # Add json to dict with survey_id as key
            E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id] = schema_metadata_response.json()
            # Verify there are 2 metadata entries for each survey_id
            total_versions = len(E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id])
            assert total_versions == 2
        
            # Verify schema metadata - ensure that the sds_schema_version is incremented by 1 for each schema and the title and schema_version is as expected
            for index, schema_metadata in enumerate(E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id]):
                expected_schema = self.test_schemas[index]
                assert schema_metadata == {
                    "guid": schema_metadata["guid"],
                    "survey_id": survey_id,
                    "schema_location": f"{survey_id}/{schema_metadata['guid']}.json",
                    "sds_schema_version": total_versions - index,
                    "sds_published_at": schema_metadata["sds_published_at"],
                    "schema_version": expected_schema["properties"]["schema_version"]["const"],
                    "title": expected_schema["title"],
                }


    @pytest.mark.order(3)
    def test_get_schema_v1(self):
        """
        Test the GET /v1/schema endpoint by retrieving the schema both by version and latest version and checking the response.

        * We retrieve the first version of the schema and check the response
        * We retrieve the latest version of the schema and check the response
        """
        for survey_id in test_survey_id_list:

            # Verify schema retrieval by version
            set_version_schema_response = self.session.get(
                f"{config.API_URL}/v1/schema?"
                f"survey_id={survey_id}&version=1",
                headers=self.headers,
            )

            assert set_version_schema_response.status_code == 200
            assert set_version_schema_response.json() == self.test_schemas[1]

            # verify schema retrieval by latest version
            latest_version_schema_response = self.session.get(
                f"{config.API_URL}/v1/schema?survey_id={survey_id}",
                headers=self.headers,
            )
            assert latest_version_schema_response.status_code == 200
            assert latest_version_schema_response.json() == self.test_schemas[0]
        

    @pytest.mark.order(4)
    def test_get_schema_v2(self):
        """
        Test the GET /v2/schema endpoint by retrieving the schema by GUID and checking the response.

        * We retrieve the schema by GUID and check the response compared to the expected schema
        """
        for survey_id in test_survey_id_list:
            for index, schema_metadata in enumerate(E2ESchemaIntegrationTest.schema_metadatas_dict[survey_id]):
                # Verify schema retrieval by GUID
                set_guid_schema_response = self.session.get(
                    f"{config.API_URL}/v2/schema?guid={schema_metadata['guid']}",
                    headers=self.headers,
                )

                assert set_guid_schema_response.status_code == 200
                assert set_guid_schema_response.json() == self.test_schemas[index]


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


class SchemaEndpointsIntegrationTest(TestCase):

    session = None
    headers = None
    invalid_token_headers = None

    @classmethod
    def setup_class(self) -> None:
        cleanup()
        self.session = setup_session()
        self.headers = generate_headers()
        self.invalid_token_headers = {"Authorization": "Bearer invalid_token"}

    @classmethod
    def teardown_class(self) -> None:
        cleanup()

    @pytest.mark.order(1)
    def test_post_schema_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for POST /v1/schema.

        * Send a request to POST /v1/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=invalid_data,
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Unauthorized access"
        else:
            print("Non-JSON Response:", response.text) 

        
    @pytest.mark.order(2)
    def test_post_schema_validation_error(self):
        """
        Test validation issue by providing invalid data for POST /v1/schema.

        * We test the POST /v1/schema endpoint by providing invalid data.
        * Assert status code: 400 Bad Request.
        """
        response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=invalid_data,
            headers=self.headers,
        )
        assert response.status_code == 400
        if "detail" in response.json():
            assert response.json()["detail"] == "Invalid data format"
        else:
            print("Response JSON:", response.json())

    @pytest.mark.order(3)
    def test_get_schema_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema for GET /v1/schema.
        
        * We send a request to the GET /v1/schema endpoint providing an invalid survey_id.
        * Assert status code: 404 Not Found.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema?survey_id={invalid_survey_id}",
            headers=self.headers,
        )
        assert response.status_code == 404
        if "detail" in response.json():
            assert response.json()["detail"] == "Schema not found"
        else:
            print("Response JSON:", response.json())

    @pytest.mark.order(4)
    def test_get_schema_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema.

        * Send a request to GET /v1/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Unauthorized access"
        else:
            print("Non-JSON Response:", response.text)  

    @pytest.mark.order(5)
    def test_get_schema_validation_error(self):
        """
        Test validation issue by providing an invalid or nonsensical survey_id for GET /v1/schema.

        * We test the GET /v1/schema endpoint by providing invalid data (missing survey_id) 
        * Assert status code: 400 Bad Request.
        * We test the GET /v1/schema endpoint by providing invalid data (nonsensical parameter)
        * Assert status code: 400 Bad Request.
        """
        # Test missing survey_id
        response = self.session.get(
            f"{config.API_URL}/v1/schema",
            headers=self.headers,
        )
        assert response.status_code == 400
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Missing required parameter"
        else:
            print("Non-JSON Response:", response.text)

        # Test Nonsensical parameter
        response = self.session.get(
        f"{config.API_URL}/v1/schema_metadata?randomparam=nonsense",
        headers=self.headers,
        )
        assert response.status_code == 400
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Invalid search" 
        else:
            print("Non-JSON Response:", response.text)

    @pytest.mark.order(6)
    def test_get_schema_metadata_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema_metadata.

        * Send a request to GET /v1/schema_metadata with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata?survey_id={test_survey_id}",
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Unauthorized access"
        else:
            print("Non-JSON Response:", response.text)  

    @pytest.mark.order(7)
    def test_get_schema_metadata_validation_error(self):
        """
        Test validation issue by providing an invalid data for GET /v1/schema_metadata.
        * Assert status code: 400 Bad Request.
        Test the GET /v1/schema_metadata endpoint by providing nonsensical parameter
        * Assert status code: 400 Bad Request.
        """
        #Missing survey_id
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata",
            headers=self.headers,
        )
        assert response.status_code == 400
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Invalid search provided" 
        else:
            print("Non-JSON Response:", response.text)

        #Nonsensical parameter
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata?invalidparam=123",
            headers=self.headers,
        )
        assert response.status_code == 400
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Invalid search provided"
        else:
            print("Non-JSON Response:", response.text)

    @pytest.mark.order(8)
    def test_get_schema_metadata_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema metadata for GET /v1/schema_metadata.

        * We send a request to the GET /v1/schema_metadata endpoint providing an invalid survey_id.
        * Assert status code: 404 Not Found.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata?survey_id={invalid_survey_id}",
            headers=self.headers,
        )
        assert response.status_code == 404
        if "detail" in response.json():
            assert response.json()["detail"] == "Schema metadata not found"
        else:
            print("Response JSON:", response.json())        

    @pytest.mark.order(9)
    def test_get_schema_v2_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v2/schema.

        * Send a request to GET /v2/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        response = self.session.get(
            f"{config.API_URL}/v2/schema?guid=invalid_guid",
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Unauthorized access"
        else:
            print("Non-JSON Response:", response.text)

    @pytest.mark.order(10)
    def test_get_schema_v2_validation_error(self):
        """
        Test validation issue by providing an invalid GUID for GET /v2/schema.

        * We test the GET /v2/schema endpoint by providing an invalid GUID.
        * Assert status code: 400 Bad Request.
        """
        response = self.session.get(
            f"{config.API_URL}/v2/schema",
            headers=self.headers,
        )
        assert response.status_code == 400
        if "detail" in response.json():
            assert response.json()["detail"] == "Invalid guid format"
        else:
            print("Response JSON:", response.json())

    @pytest.mark.order(11)
    def test_get_schema_v2_404_not_found(self):
        """
        Test data not found by requesting a nonexistent GUID for GET /v2/schema.

        * We send a request to the GET /v2/schema endpoint providing an invalid GUID.
        * Assert status code: 404 Not Found.
        """
        response = self.session.get(
            f"{config.API_URL}/v2/schema?guid=nonexistent_guid",
            headers=self.headers,
        )
        assert response.status_code == 404
        if "detail" in response.json():
            assert response.json()["detail"] == "Schema not found"
        else:
            print("Response JSON:", response.json())