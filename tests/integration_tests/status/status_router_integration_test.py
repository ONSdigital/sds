from fastapi import status
import pytest

from app.config import settings

from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_config.endpoints import ENDPOINTS, GET_STATUS
from tests.test_config.endpoints_loader import EndpointsLoader

endpoints_loader = EndpointsLoader(ENDPOINTS)


class TestHttpGetDeploymentStatus:
    

    def test_endpoint_returns_right_response_if_deployment_successful(self):
        """
        Endpoint should return `HTTP_200_OK` and the right response if the deployment is successful

        - Sends a GET request to the /status endpoint
        - Asserts the response status code is 200
        - Asserts the response body contains the right version and status
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_STATUS,
        )

        status_response = make_iap_request(method, url)

        response_as_json = status_response.json()

        assert status_response.status_code == status.HTTP_200_OK
        assert response_as_json["version"] == settings.SDS_APPLICATION_VERSION
        assert response_as_json["status"] == "OK"


    def test_endpoint_returns_unauthorized_request(self):
        """
        Endpoint should return a 401 unauthorized error if the endpoint is requested with an unauthorized token.

        - Sends a GET request to the /status endpoint with an unauthorized token
        - Asserts the response status code is 401
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_endpoint_returns_unauthorized_request on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_STATUS,
        )

        status_response = make_iap_request(
            method=method,
            path=url,
            unauthenticated=True
        )

        assert status_response.status_code == status.HTTP_401_UNAUTHORIZED
