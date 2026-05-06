from unittest.mock import MagicMock

from app.services.schema.schema_processor_service import SchemaProcessorService
from tests.test_data import schema_test_data


def test_get_survey_id_map_200_response(test_client):
    """
    When the list of Survey IDs is fetched successfully, the API must return the correct response with 200 status code
    """
    SchemaProcessorService.survey_id_map = MagicMock()
    SchemaProcessorService.get_survey_id_map.return_value = (
        schema_test_data.test_survey_id_map
    )
    response = test_client.get("/v1/survey_list")

    assert response.status_code == 200
    assert response.json() == schema_test_data.test_survey_id_map


def test_get_survey_id_map_404_response(test_client):
    """
    When the list of Survey IDs is empty, the API must return the error response with 404 status code
    """
    SchemaProcessorService.get_survey_id_map = MagicMock()
    SchemaProcessorService.get_survey_id_map.return_value = []
    response = test_client.get("/v1/survey_list")

    assert response.status_code == 404
    assert response.json()["message"] == "No Survey IDs found"


def test_get_survey_id_map_500_response(test_client_no_server_exception):
    """
    If the app encounters a global exception, the API must return the error response with 500 status code
    """
    SchemaProcessorService.get_survey_id_map = MagicMock(side_effect=Exception)

    response = test_client_no_server_exception.get("/v1/survey_list")

    assert response.status_code == 500
    assert response.json()["message"] == "Unable to process request"
