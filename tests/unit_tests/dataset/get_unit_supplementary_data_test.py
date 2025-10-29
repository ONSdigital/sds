from unittest.mock import MagicMock

from app.repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from tests.test_data import shared_test_data, dataset_test_data


def test_get_unit_supplementary_data_200_response(test_client):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """
    DatasetFirebaseRepository.get_unit_supplementary_data = MagicMock()
    DatasetFirebaseRepository.get_unit_supplementary_data.return_value = (
        dataset_test_data.unit_supplementary_data
    )

    response = test_client.get(
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}",
    )

    DatasetFirebaseRepository.get_unit_supplementary_data.assert_called_once_with(
        shared_test_data.test_guid,
        dataset_test_data.identifier,
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
        f"/v1/unit_data?dataset_id={shared_test_data.test_guid}&identifier={dataset_test_data.identifier}"
    )

    DatasetFirebaseRepository.get_unit_supplementary_data.assert_called_once_with(
        shared_test_data.test_guid,
        dataset_test_data.identifier,
    )

    assert response.status_code == 404
