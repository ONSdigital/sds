from unittest.mock import MagicMock

from fastapi import status
from app.services.shared.utility_functions import UtilityFunctions
from tests.test_config.endpoints import ENDPOINTS, GET_STATUS
from tests.test_config.endpoints_loader import EndpointsLoader

endpoints_loader = EndpointsLoader(ENDPOINTS)


def test_endpoint_returns_200_if_deployment_successful(test_client):
    """
    Endpoint should return `HTTP_200_OK` if the deployment is successful
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_STATUS,
    )

    assert response.status_code == status.HTTP_200_OK


def test_endpoint_returns_right_message_if_deployment_successful(test_client):
    """
    Endpoint should return the right response if the deployment is successful
    """
    # mocked `settings` to set the CIR_APPLICATION_VERSION to dev-048783a4
    UtilityFunctions.get_application_version = MagicMock()
    UtilityFunctions.get_application_version.return_value = "dev-048783a4"
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_STATUS,
    )
    expected_message = '{"version":"dev-048783a4","status":"OK"}'
    assert expected_message in response.content.decode("utf-8")


def test_endpoint_returns_500_if_deployment_successful(test_client):
    """
    Endpoint should return `HTTP_500_INTERNAL_SERVER_ERROR` if the env var is
    None due to a unsuccessful deployment
    """
    # mocked `settings` to set the SDS_APPLICATION_VERSION to None
    UtilityFunctions.get_application_version = MagicMock()
    UtilityFunctions.get_application_version.return_value = None
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_STATUS,
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    expected_message = '{"message":"Internal server error","status":"error"}'
    assert expected_message in response.content.decode("utf-8")
