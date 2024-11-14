from unittest import TestCase
import pytest
from src.app.config.config_factory import config
from src.integration_tests.helpers.integration_helpers import (
    cleanup,
    generate_headers,
    pubsub_setup,
    pubsub_teardown,
    setup_session,
    inject_wait_time,
    is_json_response,
)
from src.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from src.test_data.schema_test_data import test_survey_id
from src.test_data.shared_test_data import test_schema_subscriber_id
from src.test_data.schema_test_data import invalid_survey_id, invalid_data

class E2ESchemaIntegrationUnhappyPaths(TestCase):
    session = None
    headers = None
    invalid_token_headers = None

    @classmethod
    def setup_class(self) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
        inject_wait_time(3) 
        self.session = setup_session()
        self.headers = generate_headers()
        self.invalid_token_headers = {"Authorization": "Bearer invalid_token"}

    @classmethod
    def teardown_class(self) -> None:
        cleanup()
        inject_wait_time(3) # Allow all messages to process
        pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)

    @pytest.mark.order(1)
    def test_post_schema_unauthorized(self):
        response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=invalid_data,
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401
        if is_json_response(self, response) and "detail" in response.json():
            assert response.json()["detail"] == "Unauthorized access"
        else:
            print("Non-JSON Response:", response.text)  # For debugging non-JSON responses

        
    @pytest.mark.order(2)
    def test_post_schema_validation_error(self):
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
        * Expected: 400 Bad Request.
        """
        # Case 1: Missing survey_id
        response = self.session.get(
            f"{config.API_URL}/v1/schema",
            headers=self.headers,
        )
        assert response.status_code == 400
        if response.status_code == 400 and is_json_response(self, response):
            assert "Missing required parameter" in response.json()["detail"]

        # Case 2: Nonsensical parameter
        response = self.session.get(
            f"{config.API_URL}/v1/schema?randomparam=nonsense",
            headers=self.headers,
        )
        assert response.status_code == 400
        if response.status_code == 400 and is_json_response(self, response):
            assert "Invalid parameter" in response.json()["detail"]

    @pytest.mark.order(6)
    def test_get_schema_metadata_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema_metadata.
        * Expected: 401 Unauthorized.
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
        Test validation issue by providing an invalid or nonsensical survey_id for GET /v1/schema_metadata.
        * Expected: 400 Bad Request.
        """
        # Case 1: Missing survey_id
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata",
            headers=self.headers,
        )
        assert response.status_code == 400
        if is_json_response(self, response):
            json_response = response.json()
            if "status" in json_response and "message" in json_response:
                assert json_response["status"] == "error"
                assert json_response["message"] == "Invalid search provided"
            else:
                print("Unexpected response structure:", json_response)
        else:
            print("Non-JSON Response:", response.text)

        # Case 2: Nonsensical parameter
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata?invalidparam=123",
            headers=self.headers,
        )
        assert response.status_code == 400
        if is_json_response(self, response):
            json_response = response.json()
            if "status" in json_response and "message" in json_response:
                assert json_response["status"] == "error"
                assert json_response["message"] == "Invalid search provided"
            else:
                print("Unexpected response structure:", json_response)
        else:
            print("Non-JSON Response:", response.text)


    @pytest.mark.order(8)
    def test_get_schema_metadata_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema metadata for GET /v1/schema_metadata.
        * Expected: 404 Not Found.
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
        * Expected: 401 Unauthorized.
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
        * Expected: 400 Bad Request.
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
        * Expected: 404 Not Found.
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