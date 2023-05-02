from unittest.mock import MagicMock

from repositories.dataset_repository import DatasetRepository

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


def test_get_dataset_metadata_collection_200_response(test_client):
    """
    When the schema metadata is retrieved successfully there should be a log before and after.
    """
    DatasetRepository.get_dataset_metadata_collection = MagicMock()
    DatasetRepository.get_dataset_metadata_collection.return_value = (
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


def test_get_dataset_metadata_collection_200_response(test_client):
    """
    When the schema metadata is retrieved successfully there should be a log before and after.
    """
    DatasetRepository.get_dataset_metadata_collection = MagicMock()
    DatasetRepository.get_dataset_metadata_collection.return_value = []

    response = test_client.get("/v1/dataset_metadata?survey_id=xzy&period_id=abc")

    assert response.status_code == 404
