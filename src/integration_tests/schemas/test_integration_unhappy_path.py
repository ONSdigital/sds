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
)
from src.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from src.test_data.schema_test_data import test_survey_id
from src.test_data.shared_test_data import test_schema_subscriber_id

class E2ESchemaIntegrationUnhappyPaths(TestCase):
    session = None
    headers = None
    invalid_survey_id = "nonexistent_survey"
    invalid_data = {"invalid": "data"}
    invalid_token_headers = None

    @classmethod
    def setup_class(cls) -> None:
        cleanup()
        pubsub_setup(schema_pubsub_helper, test_schema_subscriber_id)
        inject_wait_time(3) 
        cls.session = setup_session()
        cls.headers = generate_headers()
        cls.invalid_token_headers = {"Authorization": "Bearer invalid_token"}

    @classmethod
    def teardown_class(cls) -> None:
        cleanup()
        inject_wait_time(3) # Allow all messages to process
        pubsub_teardown(schema_pubsub_helper, test_schema_subscriber_id)

    @pytest.mark.order(1)
    def test_post_schema_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for POST /v1/schema.
        * Expected: 401 Unauthorized.
        """
        response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=self.invalid_data,
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401

    @pytest.mark.order(2)
    def test_post_schema_validation_error(self):
        """
        Test validation issue by providing invalid data for POST /v1/schema.
        * Expected: 400 Bad Request.
        """
        response = self.session.post(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            json=self.invalid_data,
            headers=self.headers,
        )
        assert response.status_code == 400

    @pytest.mark.order(3)
    def test_get_schema_404_not_found(self):
        """
        Test data not found by requesting a nonexistent schema ID for GET /v1/schema.
        * Expected: 404 Not Found.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema?survey_id={self.invalid_survey_id}",
            headers=self.headers,
        )
        assert response.status_code == 404

    @pytest.mark.order(4)
    def test_get_schema_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema.
        * Expected: 401 Unauthorized.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema?survey_id={test_survey_id}",
            headers=self.invalid_token_headers,
        )
        assert response.status_code == 401

    @pytest.mark.order(5)
    def test_get_schema_validation_error(self):
        """
        Test validation issue by providing an invalid survey_id for GET /v1/schema.
        * Expected: 400 Bad Request.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema",
            headers=self.headers,
        )
        assert response.status_code == 400

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

    @pytest.mark.order(7)
    def test_get_schema_metadata_validation_error(self):
        """
        Test validation issue by providing an invalid survey_id for GET /v1/schema_metadata.
        * Expected: 400 Bad Request.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata",
            headers=self.headers,
        )
        assert response.status_code == 400

    @pytest.mark.order(8)
    def test_get_schema_metadata_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema metadata for GET /v1/schema_metadata.
        * Expected: 404 Not Found.
        """
        response = self.session.get(
            f"{config.API_URL}/v1/schema_metadata?survey_id={self.invalid_survey_id}",
            headers=self.headers,
        )
        assert response.status_code == 404

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