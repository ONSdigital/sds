from unittest.mock import MagicMock

from fastapi import status

from tests.test_data import schema_test_data
from tests.unit_tests.helpers.firestore_helpers import setup_mock_data


def test_get_schema_metadata_collection_200_response(schema_collection_mock, test_client):
    """
    When the schema metadata is successfully retrieved there should be a 200 status code and expected response contains
    only the schema metadata satisfying the query parameters (survey_id)
    """
    # Set up mock data to simulate existing 2 schema metadata in the collection
    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_1.__dict__,
        mock_guid=schema_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_2.__dict__,
        mock_guid=schema_test_data.test_guid_2,
    )

    # Set up mock data to simulate existing schema metadata for another survey in the collection
    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_other.__dict__,
        mock_guid=schema_test_data.test_guid_3,
    )

    response = test_client.get(f"/v1/schema_metadata?survey_id={schema_test_data.test_survey_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [schema_metadata.__dict__ for schema_metadata in schema_test_data.test_schema_metadata]


def test_get_schema_metadata_with_incorrect_key(test_client):
    """
    Checks that fastAPI return 400 error with appropriate msg
    when incorrect key is used to query schema metadata
    at get_schemas_metadata endpoint
    """
    response = test_client.get("/v1/schema_metadata?incorrect_key=123")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Invalid search provided"


def test_get_schema_metadata_with_not_found_error(test_client):
    """
    Checks that fastAPI return 404 error with appropriate msg
    when schema metadata is not found at get_schemas_metadata
    endpoint
    """
    response = test_client.get(f"/v1/schema_metadata?survey_id={schema_test_data.test_survey_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No results found"


def test_get_all_schema_metadata_collection_200_response(schema_collection_mock, test_client):
    """
    When the schema metadata is successfully retrieved there should be a 200 status code and expected response contains
    all schema metadata in FireStore
    """
    # Set up mock data to simulate existing 2 schema metadata in the collection
    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_1.__dict__,
        mock_guid=schema_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_2.__dict__,
        mock_guid=schema_test_data.test_guid_2,
    )

    # Set up mock data to simulate existing schema metadata for another survey in the collection
    setup_mock_data(
        mock_collection=schema_collection_mock,
        mock_data=schema_test_data.test_schema_metadata_other.__dict__,
        mock_guid=schema_test_data.test_guid_3,
    )

    response = test_client.get("/v1/all_schema_metadata")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [schema_metadata.__dict__ for schema_metadata in schema_test_data.test_all_schema_metadata]


def test_get_all_schema_metadata_collection_404_response(test_client):
    """
    When the schema metadata collection is not found in firestore there should be a 404 status code and expected response.
    """
    response = test_client.get("/v1/all_schema_metadata")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No results found"


def test_global_error(firestore_mock, test_client_no_server_exception):
    """
    Checks that if app encounter a global exception error
    fastAPI will return a 500 exception with appropriate msg
    Func get_schema_metadata is patched and raised with exception
    Fixture client_no_server_exception is used to avoid exiting
    the test at exception so that the response can be validated
    """
    firestore_mock.get_schemas_collection = MagicMock(side_effect=Exception)

    response = test_client_no_server_exception.get(
        f"/v1/schema_metadata?survey_id={schema_test_data.test_survey_id}"
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"

    response = test_client_no_server_exception.get(
        f"/v1/all_schema_metadata"
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"
