from unittest.mock import MagicMock

from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


def test_get_dataset_metadata_collection_200_response(test_client):
    """
    When the dataset metadata is retrieved successfully there should be a 200 status code and response data.
    """
    DatasetFirebaseRepository.get_dataset_metadata_collection = MagicMock()
    DatasetFirebaseRepository.get_dataset_metadata_collection.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            dataset_test_data.dataset_metadata_collection_no_id
        )
    )

    expected = [
        {
            "dataset_id": "id_0",
            **dataset_test_data.dataset_metadata_collection_no_id[0],
        },
        {
            "dataset_id": "id_1",
            **dataset_test_data.dataset_metadata_collection_no_id[1],
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
