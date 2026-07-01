from unittest.mock import MagicMock
from fastapi import status

from tests.test_config.endpoints import ENDPOINTS, GET_DATASET_METADATA, GET_ALL_DATASET_METADATA
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data import dataset_test_data, shared_test_data
from tests.unit_tests.helpers.firestore_helpers import setup_mock_data

endpoints_loader = EndpointsLoader(ENDPOINTS)


def test_get_dataset_metadata_collection_200_response(dataset_collection_mock, test_client):
    """
    When the dataset metadata is retrieved successfully there should be a 200 status code and expected response contains
    only the dataset metadata satisfying the query parameters (survey_id and period id)
    """
    # Set up mock data to simulate existing 2 dataset metadata in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_1.__dict__,
        mock_guid=shared_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_2.__dict__,
        mock_guid=shared_test_data.test_guid_2,
    )

    # Set up mock data to simulate existing dataset metadata for another survey in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_other.__dict__,
        mock_guid=shared_test_data.test_guid_3,
    )

    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_DATASET_METADATA,
        params={
            "survey_id": dataset_test_data.test_survey_id,
            "period_id": dataset_test_data.test_period_id
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [dataset_metadata.__dict__ for dataset_metadata in dataset_test_data.test_dataset_metadata]


def test_get_all_dataset_metadata_collection_200_response(dataset_collection_mock, test_client):
    """
    When the dataset metadata collection is retrieved successfully there should be a 200 status code and expected response
    contains all dataset metadata in the collection regardless of survey id and period id
    """
    # Set up mock data to simulate existing 2 dataset metadata in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_1.__dict__,
        mock_guid=shared_test_data.test_guid,
    )

    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_2.__dict__,
        mock_guid=shared_test_data.test_guid_2,
    )

    # Set up mock data to simulate existing dataset metadata for another survey in the collection
    setup_mock_data(
        mock_collection=dataset_collection_mock,
        mock_data=dataset_test_data.test_dataset_metadata_other.__dict__,
        mock_guid=shared_test_data.test_guid_3,
    )

    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_ALL_DATASET_METADATA,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [dataset_metadata.__dict__ for dataset_metadata in dataset_test_data.test_all_dataset_metadata]


def test_get_all_dataset_metadata_collection_404_response(test_client):
    """
    When no dataset metadata is retrieved from all dataset metadata endpoint there should be a 404 response.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_ALL_DATASET_METADATA,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No datasets found"


def test_get_dataset_metadata_collection_404_response(test_client):
    """
    When no dataset metadata is retrieved dataset metadata endpoint there should be a 404 response.
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_DATASET_METADATA,
        params={
            "survey_id": dataset_test_data.test_survey_id,
            "period_id": dataset_test_data.test_period_id
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "No datasets found"


def test_get_dataset_metadata_with_invalid_parameters(test_client):
    """
    Checks that fastAPI does not accept invalid parameters/
    non-numeric version and returns a 400 error with appropriate message at
    dataset_metadata endpoint
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_DATASET_METADATA,
        params={
            "invalid_key": "076",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Invalid search parameters provided"


def test_get_dataset_metadata_with_invalid_extra_parameters(test_client):
    """
    Checks that fastAPI does not accept invalid parameters/
    non-numeric version and returns a 400 error with appropriate message at
    dataset_metadata endpoint
    """
    response = endpoints_loader.send_request(
        client=test_client,
        key=GET_DATASET_METADATA,
        params={
            "survey_id": "076",
            "invalid_key": "456",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Invalid search parameters provided"


def test_global_error(firestore_mock, test_client_no_server_exception):
    """
    Checks that if app encounter a global exception error
    fastAPI will return a 500 exception with appropriate msg
    Func get_schema_metadata is patched and raised with exception
    Fixture client_no_server_exception is used to avoid exiting
    the test at exception so that the response can be validated
    """
    firestore_mock.get_datasets_collection = MagicMock(side_effect=Exception)

    response = endpoints_loader.send_request(
        client=test_client_no_server_exception,
        key=GET_DATASET_METADATA,
        params={
            "survey_id": dataset_test_data.test_survey_id,
            "period_id": dataset_test_data.test_period_id
        },
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"

    response = endpoints_loader.send_request(
        client=test_client_no_server_exception,
        key=GET_ALL_DATASET_METADATA,
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "Unable to process request"
