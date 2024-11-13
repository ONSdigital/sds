from unittest.mock import MagicMock
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.dataset.dataset_service import DatasetService
from src.test_data import dataset_test_data, shared_test_data


def test_get_unit_supplementary_data_200_response(test_client):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """
    DatasetService.get_dataset_metadata_collection = MagicMock()
    DatasetService.get_dataset_metadata_collection.return_value = dataset_test_data.unit_supplementary_data
    DatasetFirebaseRepository.get_unit_supplementary_data = MagicMock()
    DatasetFirebaseRepository.get_unit_supplementary_data.return_value = (
        dataset_test_data.unit_supplementary_data
    )

    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}",
    )

    assert response.status_code == 200
    assert response.json() == dataset_test_data.unit_supplementary_data


def test_get_unit_supplementary_data_404_response(test_client):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """
    DatasetService.get_dataset_metadata_collection = MagicMock()
    DatasetService.get_dataset_metadata_collection.return_value = None
    DatasetFirebaseRepository.get_unit_supplementary_data = MagicMock()
    DatasetFirebaseRepository.get_unit_supplementary_data.return_value = None

    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}"
    )

    assert response.status_code == 404
