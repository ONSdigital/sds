from unittest.mock import MagicMock

from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from src.test_data import dataset_test_data


def test_get_dataset_metadata_collection_200_response(test_client):
    """
    When the dataset metadata is retrieved successfully there should be a 200 status code and response data.
    """
    DatasetFirebaseRepository.get_dataset_metadata_collection = MagicMock()
    DatasetFirebaseRepository.get_dataset_metadata_collection.return_value = (
        dataset_test_data.dataset_metadata_collection
    )

    expected = [
        {
            **dataset_test_data.dataset_metadata_collection[0],
        },
        {
            **dataset_test_data.dataset_metadata_collection[1],
        },
    ]

    response = test_client.get("/v1/dataset_metadata?survey_id=xzy&period_id=abc")

    assert response.status_code == 200
    assert response.json() == expected


def test_get_dataset_metadata_collection_404_response(test_client):
    """
    When no dataset metadata is retrieved there should be a 404 response.
    """
    DatasetFirebaseRepository.get_dataset_metadata_collection = MagicMock()
    DatasetFirebaseRepository.get_dataset_metadata_collection.return_value = []

    response = test_client.get("/v1/dataset_metadata?survey_id=xzy&period_id=abc")

    assert response.status_code == 404
    assert response.json()["message"] == "No datasets found"


def test_get_dataset_metadata_with_invalid_parameters(test_client):
    """
    Checks that fastAPI does not accept invalid porameters/
    non-numeric version and returns a 400 error with appropriate message at
    dataset_metadata endpoint
    """
    response = test_client.get("/v1/dataset_metadata?invalid_key=076")

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid search parameters provided"


def test_get_dataset_metadata_with_invalid_extra_parameters(test_client):
    """
    Checks that fastAPI does not accept invalid porameters/
    non-numeric version and returns a 400 error with appropriate message at
    dataset_metadata endpoint
    """
    response = test_client.get("/v1/dataset_metadata?survey_id=076&invalid_key=456")

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid search parameters provided"
