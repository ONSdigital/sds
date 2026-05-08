from unittest.mock import MagicMock

from fastapi import status

from tests.test_data import shared_test_data, dataset_test_data
from tests.unit_tests.helpers.firestore_helpers import setup_mock_data


def test_get_unit_supplementary_data_200_response(dataset_collection_mock, test_client):
    """
    When the unit supplementary data is successfully retrieved there should be a 200 status code and expected response
    contains the unit supplementary data matching the query parameters (dataset_id and identifier)
    """
    # Set up mock data to simulate existing dataset metadata and unit data model in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_1.__dict__,
        mock_guid=shared_test_data.test_guid,
        sub_collection_name=dataset_test_data.sub_collection_name,
        sub_collection_data=dataset_test_data.test_unit_data.__dict__,
        sub_collection_guid=dataset_test_data.identifier
    )

    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dataset_test_data.test_unit_data.__dict__


def test_get_unit_supplementary_data_404_response(test_client):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """
    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No unit data found"


def test_get_unit_supplementary_data_with_incorrect_key(test_client):
    """
    Checks that fastAPI return 400 error with appropriate msg
    when incorrect key is used to query unit supplementary data
    at get_unit_supplementary_data endpoint
    """
    response = test_client.get(f"/v1/unit_data?incorrect_key=123")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Validation has failed"


def test_global_error(firestore_mock, test_client_no_server_exception):
    """
    Checks that if app encounter a global exception error
    fastAPI will return a 500 exception with appropriate msg
    Func get_schema_metadata is patched and raised with exception
    Fixture client_no_server_exception is used to avoid exiting
    the test at exception so that the response can be validated
    """
    firestore_mock.get_datasets_collection = MagicMock(side_effect=Exception)

    response = test_client_no_server_exception.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}"
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"
