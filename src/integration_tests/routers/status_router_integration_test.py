from fastapi import status
from unittest import TestCase
from src.integration_tests.helpers.integration_helpers import (
    generate_headers,
    setup_session,
)
from src.app.config.config_factory import config

class TestHttpGetDeploymentStatus(TestCase):
    def test_endpoint_returns_right_response_if_deployment_successful(self):
        """
        Endpoint should return `HTTP_200_OK` and the right response if the deployment is successful
        """
        session = setup_session()
        headers = generate_headers()

        status_response = session.get(
            f"{config.API_URL}/status",
            headers=headers,
        )
        response_as_json = status_response.json()
        assert status_response.status_code == status.HTTP_200_OK
        assert response_as_json["version"] == config.SDS_APPLICATION_VERSION
        assert response_as_json["status"] == "OK"

    def test_endpoint_returns_unauthorized_request(self):
        """
        Endpoint should return a 401 unauthorized error if the endpoint is requested with an unauthorized token.
        """
        if config.OAUTH_CLIENT_ID.__contains__("local"):
            pass
        else:
            session = setup_session()
            headers = {"Authorization": "Bearer bad-request-key", "Content-Type": "application/json"}

            status_response = session.get(
                f"{config.API_URL}/status",
                headers=headers,
            )

            assert status_response.status_code == status.HTTP_401_UNAUTHORIZED
