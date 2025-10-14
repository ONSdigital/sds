from unittest import TestCase

from fastapi import status
import pytest

from app.config.config_factory import config
from integration_tests.helpers.integration_helpers import (
    generate_headers,
    setup_session,
)


class TestHttpGetDeploymentStatus(TestCase):
    
    @pytest.mark.order(1)
    def test_endpoint_returns_right_response_if_deployment_successful(self):
        """
        Endpoint should return `HTTP_200_OK` and the right response if the deployment is successful

        - Sends a GET request to the /status endpoint
        - Asserts the response status code is 200
        - Asserts the response body contains the right version and status
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


    @pytest.mark.order(2)
    def test_endpoint_returns_unauthorized_request(self):
        """
        Endpoint should return a 401 unauthorized error if the endpoint is requested with an unauthorized token.

        - Sends a GET request to the /status endpoint with an unauthorized token
        - Asserts the response status code is 401
        """
        if config.OAUTH_CLIENT_ID.__contains__("local"):
            pass
        else:
            session = setup_session()
            headers = {
                "Authorization": "Bearer bad-request-key",
                "Content-Type": "application/json",
            }

            status_response = session.get(
                f"{config.API_URL}/status",
                headers=headers,
            )

            assert status_response.status_code == status.HTTP_401_UNAUTHORIZED
