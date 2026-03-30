import pytest

from app.config import settings
from tests.integration_tests.helpers.integration_helpers import (
    cleanup,
    pubsub_setup,
    pubsub_teardown,
    pubsub_purge_messages,
    inject_wait_time,
    is_json_response,
)
from tests.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_data.schema_test_data import test_survey_id_map
from tests.test_data.shared_test_data import test_schema_subscriber_id, test_survey_id_list
from tests.test_data.schema_test_data import invalid_survey_id, invalid_data, test_survey_id


class TestSchemaEndpoints:

    def setup_method(self) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
        inject_wait_time(3) # Inject wait time to allow resources properly set up


    def teardown_method(self) -> None:
        cleanup()
        inject_wait_time(3) # Inject wait time to allow all message to be processed
        pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)


    def test_post_schema_v1(self, test_schema_list):
        """
        Test the POST /v1/schema endpoint by publishing schemas from test_survey_id_list and checking the response
        and the pub/sub message.

        * We post a schema for each survey_id in survey_id_list and check the response
        * We retrieve and verify received messages from Pub/Sub
        """
        # Post v1 schema for each survey_id - v1 is stored in the second index of the test_schemas list
        for survey_id in test_survey_id_list:

            schema_post_response = make_iap_request(
                "POST",
                f"/v1/schema?survey_id={survey_id}",
                json=test_schema_list[1]
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

            schema_post_response = make_iap_request(
                "POST",
                f"/v1/schema?survey_id={survey_id}",
                json=test_schema_list[0]
            )

            assert schema_post_response.status_code == 200
            assert "guid" in schema_post_response.json()

            received_messages = schema_pubsub_helper.pull_and_acknowledge_messages(
                test_schema_subscriber_id
            )

            # Retrieve and verify received messages from Pub/Sub
            received_messages_json = received_messages[0]
            assert received_messages_json == schema_post_response.json()


    def test_get_schema_metadata_v1(self, post_schema, test_schema_list):
        """
        Test the GET /v1/schema_metadata endpoint by retrieving the schema metadata for each test_survey_id
        and checking the response.

        * We retrieve and verify schema metadata
        """

        for survey_id in test_survey_id_list:
            schema_metadata_response = make_iap_request(
                "GET",
                f"/v1/schema_metadata?survey_id={survey_id}"
            )

            assert schema_metadata_response.status_code == 200
            schema_metadata_list = schema_metadata_response.json()
            # Verify there are 2 metadata entries for each survey_id
            total_versions = len(schema_metadata_list)
            assert total_versions == 2
        
            # Verify schema metadata - ensure that the sds_schema_version is incremented by 1 for each schema
            # and the title and schema_version is as expected.
            for index, schema_metadata in enumerate(schema_metadata_list):
                expected_schema = test_schema_list[index]
                assert schema_metadata == {
                    "guid": schema_metadata["guid"],
                    "survey_id": survey_id,
                    "schema_location": f"{survey_id}/{schema_metadata['guid']}.json",
                    "sds_schema_version": total_versions - index,
                    "sds_published_at": schema_metadata["sds_published_at"],
                    "schema_version": expected_schema["properties"]["schema_version"]["const"],
                    "title": expected_schema["title"],
                }

        pubsub_purge_messages(schema_pubsub_helper, test_schema_subscriber_id)


    def test_get_all_schema_metadata_v1(self, post_schema, test_schema_list):
        """
        Test the GET /v1/schema_metadata endpoint by retrieving all schema metadata and checking the response.

        * We retrieve and verify all schema metadata
        """

        all_schema_metadata_response = make_iap_request(
                "GET",
                f"/v1/all_schema_metadata"
            )
        expected_schema_count = len(test_schema_list) * len(test_survey_id_list)
        assert all_schema_metadata_response.status_code == 200

        all_schema_metadata_response = all_schema_metadata_response.json()
        schemas = []
        for schema in all_schema_metadata_response:
            if schema["survey_id"] in test_survey_id_list:
                schemas.append(schema)
        assert len(schemas) == expected_schema_count

        pubsub_purge_messages(schema_pubsub_helper, test_schema_subscriber_id)


    def test_get_schema_v1(self, post_schema, test_schema_list):
        """
        Test the GET /v1/schema endpoint by retrieving the schema both by version and latest version and
        checking the response.

        * We retrieve the first version of the schema and check the response
        * We retrieve the latest version of the schema and check the response
        """
        for survey_id in test_survey_id_list:

            # Verify schema retrieval by version
            set_version_schema_response = make_iap_request(
                "GET",
                f"/v1/schema?survey_id={survey_id}&version=1"
            )

            assert set_version_schema_response.status_code == 200
            assert set_version_schema_response.json() == test_schema_list[1]

            # verify schema retrieval by latest version
            latest_version_schema_response = make_iap_request(
                "GET",
                f"/v1/schema?survey_id={survey_id}"
            )

            assert latest_version_schema_response.status_code == 200
            assert latest_version_schema_response.json() == test_schema_list[0]

        pubsub_purge_messages(schema_pubsub_helper, test_schema_subscriber_id)
        

    def test_get_schema_v2(self, post_schema, test_schema_list):
        """
        Test the GET /v2/schema endpoint by retrieving the schema by GUID and checking the response.

        * We retrieve the schema by GUID and check the response compared to the expected schema
        """
        for survey_id in test_survey_id_list:
            schema_metadata_response = make_iap_request(
                "GET",
                f"/v1/schema_metadata?survey_id={survey_id}",
            )

            schema_metadata_list = schema_metadata_response.json()

            for index, schema_metadata in enumerate(schema_metadata_list):
                # Verify schema retrieval by GUID
                set_guid_schema_response = make_iap_request(
                    "GET",
                    f"/v2/schema?guid={schema_metadata['guid']}"
                )

                assert set_guid_schema_response.status_code == 200
                assert set_guid_schema_response.json() == test_schema_list[index]

        pubsub_purge_messages(schema_pubsub_helper, test_schema_subscriber_id)


    def test_survey_id_map(self):
        """
        Retrieve survey mapping data using the /survey_list endpoint.
        Verify that the retrieved data matches the expected survey mapping data.

        * We retrieve the survey mapping data and check the response
        """

        set_survey_id_map_response = make_iap_request(
            "GET",
            f"/v1/survey_list"
        )

        assert set_survey_id_map_response.status_code == 200
        assert set_survey_id_map_response.json() == test_survey_id_map


    def test_post_schema_unauthorized(self, test_schema_list):
        """
        Test unauthorized access by providing incorrect authorization token for POST /v1/schema.

        * Send a request to POST /v1/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_post_schema_unauthorized on local environment")

        response = make_iap_request(
            "POST",
            f"/v1/schema?survey_id={test_survey_id}",
            json=test_schema_list[0],
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_post_schema_validation_error(self):
        """
        Test validation issue by providing invalid data for POST /v1/schema.

        * We test the POST /v1/schema endpoint by providing invalid data.
        * Assert status code: 400 Bad Request.
        """
        response = make_iap_request(
            "POST",
            f"/v1/schema?survey_id={test_survey_id}",
            json=invalid_data
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()

        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Validation has failed", f"Unexpected message: {response_data['message']}"


    def test_get_schema_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema for GET /v1/schema.
        
        * We send a request to the GET /v1/schema endpoint providing an invalid survey_id.
        * Assert status code: 404 Not Found.
        """
        response = make_iap_request(
            "GET",
            f"/v1/schema?survey_id={invalid_survey_id}",
        )

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "No schema found", f"Unexpected message: {response_data['message']}"


    def test_get_schema_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema.

        * Send a request to GET /v1/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_schema_unauthorized on local environment")

        response = make_iap_request(
            "GET",
            f"/v1/schema?survey_id={test_survey_id}",
            unauthenticated=True
        )

        assert response.status_code == 401
    

    def test_get_schema_validation_error(self):
        """
        Test validation issue by providing an invalid or nonsensical survey_id for GET /v1/schema.

        * We test the GET /v1/schema endpoint by providing invalid data (missing survey_id) 
        * Assert status code: 400 Bad Request.
        * We test the GET /v1/schema endpoint by providing invalid data (nonsensical parameter)
        * Assert status code: 400 Bad Request.
        """
        # Test missing survey_id
        response = make_iap_request(
            "GET",
            f"/v1/schema",
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"

        # Test nonsensical parameter
        response = make_iap_request(
            "GET",
            f"/v1/schema_metadata?randomparam=nonsense",
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"


    def test_get_schema_metadata_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema_metadata.

        * Send a request to GET /v1/schema_metadata with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_schema_metadata_unauthorized on local environment")

        response = make_iap_request(
                "GET",
            f"/v1/schema_metadata?survey_id={test_survey_id}",
        )

        assert response.status_code == 401


    def test_get_schema_metadata_validation_error(self):
        """
        Test validation issue by providing an invalid data for GET /v1/schema_metadata.
        * Assert status code: 400 Bad Request.
        Test the GET /v1/schema_metadata endpoint by providing nonsensical parameter
        * Assert status code: 400 Bad Request.
        """
        #Missing survey_id
        response = make_iap_request(
            "GET",
            f"/v1/schema_metadata",
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"

        #Nonsensical parameter
        response = make_iap_request(
            "GET",
            f"/v1/schema_metadata?invalidparam=123",
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"


    def test_get_schema_metadata_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema metadata for GET /v1/schema_metadata.

        * We send a request to the GET /v1/schema_metadata endpoint providing an invalid survey_id.
        * Assert status code: 404 Not Found.
        """
        response = make_iap_request(
            "GET",
            f"/v1/schema_metadata?survey_id={invalid_survey_id}",
        )
        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "No results found", f"Unexpected message: {response_data['message']}"


    def test_get_all_schema_metadata_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/all_schema_metadata.

        * Send a request to GET /v1/all_schema_metadata with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_all_schema_metadata_unauthorized on local environment")

        response = make_iap_request(
            "GET",
            f"/v1/all_schema_metadata",
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_get_schema_v2_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v2/schema.

        * Send a request to GET /v2/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_schema_v2_unauthorized on local environment")

        response = make_iap_request(
            "GET",
            f"/v2/schema?guid=invalid_guid",
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_get_schema_v2_validation_error(self):
        """
        Test validation issue by providing an invalid GUID for GET /v2/schema.

        * We test the GET /v2/schema endpoint by providing an invalid GUID.
        * Assert status code: 400 Bad Request.
        """
        response = make_iap_request(
            "GET",
            f"/v2/schema",
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid parameter provided", f"Unexpected message: {response_data['message']}"


    def test_get_schema_v2_404_not_found(self):
        """
        Test data not found by requesting a nonexistent GUID for GET /v2/schema.

        * We send a request to the GET /v2/schema endpoint providing an invalid GUID.
        * Assert status code: 404 Not Found.
        """
        response = make_iap_request(
            "GET",
            f"/v2/schema?guid=nonexistent_guid",
        )

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "No schema found", f"Unexpected message: {response_data['message']}"
