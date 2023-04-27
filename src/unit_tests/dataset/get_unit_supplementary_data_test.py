from repositories.dataset_repository import DatasetRepository

from src.test_data.new_dataset import dataset_test_data


def test_get_unit_supplementary_data_200_response(dataset_client, dataset_repository_boundaries_mock):
    """
    The e2e journey for retrieving unit supplementary data from firestore,with repository boundaries mocked
    """
    response = dataset_client.get(
        f"/v1/unit_data?dataset_id={dataset_test_data.test_dataset_id}&unit_id={dataset_test_data.test_unit_id}"
    )

    DatasetRepository.get_unit_supplementary_data.assert_called_once_with(
        dataset_id=dataset_test_data.test_dataset_id,
        unit_id=dataset_test_data.test_unit_id,
    )

    assert response.status_code == 200
    assert response.json() == dataset_test_data.test_unit_supplementary_data
