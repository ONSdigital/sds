from unittest.mock import MagicMock

from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from src.test_data import dataset_test_data, shared_test_data


def test_get_unit_supplementary_data_200_response(test_client):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """

    DatasetFirebaseRepository.get_unit_supplementary_data = MagicMock()
    DatasetFirebaseRepository.get_unit_supplementary_data.return_value = (
        dataset_test_data.unit_supplementary_data
    )

    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&unit_id={dataset_test_data.unit_id}",
    )

    DatasetFirebaseRepository.get_unit_supplementary_data.assert_called_once_with(
        shared_test_data.test_guid,
        dataset_test_data.unit_id,
    )

    assert response.status_code == 200
    assert response.json() == dataset_test_data.unit_supplementary_data


def test_get_unit_supplementary_data_404_response(test_client):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """
    DatasetFirebaseRepository.get_unit_supplementary_data = MagicMock()
    DatasetFirebaseRepository.get_unit_supplementary_data.return_value = None

    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&unit_id={dataset_test_data.unit_id}"
    )

    DatasetFirebaseRepository.get_unit_supplementary_data.assert_called_once_with(
        shared_test_data.test_guid,
        dataset_test_data.unit_id,
    )

    assert response.status_code == 404
