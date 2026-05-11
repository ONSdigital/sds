from unittest.mock import MagicMock, Mock
from fastapi import status
import requests

from app.services.shared.utility_functions import UtilityFunctions
from tests.test_data import schema_test_data


def mock_response(status_code, json_data) -> MagicMock:
    response = Mock(spec=requests.Response)
    response.status_code = status_code
    response.json.return_value = json_data
    return response


def test_request_survey_id_mapping_200_response(test_client):
    """
    When the list of Survey IDs mapping is successfully retrieved, the API must return the response with 200 status code
    and the expected list of survey IDs mapping
    """
    UtilityFunctions.request_survey_id_mapping = MagicMock()
    UtilityFunctions.request_survey_id_mapping.return_value = mock_response(
        status_code=200,
        json_data=schema_test_data.test_survey_id_map
    )

    response = test_client.get("/v1/survey_list")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == schema_test_data.test_survey_id_map


def test_request_survey_id_mapping_empty_list_response(test_client):
    """
    When the list of Survey IDs mapping is empty, the API must return the error response with 404 status code
    """
    UtilityFunctions.request_survey_id_mapping = MagicMock()
    UtilityFunctions.request_survey_id_mapping.return_value = mock_response(
        status_code=200,
        json_data=[]
    )

    response = test_client.get("/v1/survey_list")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No Survey IDs found"


def test_request_survey_id_mapping_404_response(test_client):
    """
    When the list of Survey IDs mapping returns a non-200 response, the API must return the error response with 404 status code
    """
    UtilityFunctions.request_survey_id_mapping = MagicMock()
    UtilityFunctions.request_survey_id_mapping.return_value = mock_response(
        status_code=404,
        json_data=None
    )

    response = test_client.get("/v1/survey_list")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No Survey IDs found"


def test_get_survey_id_map_500_response(test_client_no_server_exception):
    """
    When the app encounters an exception when requesting survey ID mapping data, the API must return the error response with 500 status code
    """
    UtilityFunctions.request_survey_id_mapping = MagicMock(side_effect=Exception)

    response = test_client_no_server_exception.get("/v1/survey_list")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"
