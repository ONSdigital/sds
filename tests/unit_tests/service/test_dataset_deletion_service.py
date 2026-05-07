from unittest.mock import MagicMock
from fastapi import status

from tests.test_data import dataset_test_data


def test_process_collection_exercise_end_message_through_endpoint(
        dataset_delete_service_setup,
        test_client):
    dataset_delete_service_setup.dataset_service.get_dataset_metadata_collection = MagicMock()
    dataset_delete_service_setup.dataset_service.get_dataset_metadata_collection.return_value = (
        dataset_test_data.dataset_metadata_collection_deletion
    )

    response = test_client.post(
        "/collection-exercise-end",
        json=dataset_test_data.test_data_collection_end_input,
    )

    assert response.status_code == status.HTTP_200_OK

def test_check_if_collection_has_supplementary_data_return_true_when_dataset_id_present(dataset_delete_service_setup):

    result = dataset_delete_service_setup._check_if_collection_has_dataset_guid(
        dataset_test_data.test_data_collection_end
    )

    assert result

def test_check_if_collection_has_supplementary_data_return_false_when_dataset_id_not_present(dataset_delete_service_setup):

    result = dataset_delete_service_setup._check_if_collection_has_dataset_guid(
        dataset_test_data.test_data_collection_end_missing_id
    )

    assert not result

def test_collect_metadata_for_period_and_survey_returns_list_metadata(dataset_delete_service_setup):
    dataset_delete_service_setup.dataset_service.get_dataset_metadata_collection = MagicMock()
    dataset_delete_service_setup.dataset_service.get_dataset_metadata_collection.return_value = (
        dataset_test_data.dataset_metadata_collection_deletion
    )

    expected = [
        dataset_test_data.dataset_metadata_collection_deletion[0],
        dataset_test_data.dataset_metadata_collection_deletion[1],
    ]

    result = dataset_delete_service_setup._collect_metadata_for_period_and_survey(
        dataset_test_data.test_data_collection_end
    )

    assert result == expected
