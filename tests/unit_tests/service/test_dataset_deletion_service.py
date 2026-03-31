from unittest.mock import MagicMock, patch

from app.repositories.firebase.deletion_firebase_repository import (
    DeletionMetadataFirebaseRepository,
)
from app.services.dataset.dataset_deletion_service import DatasetDeletionService
from app.services.dataset.dataset_service import DatasetService

from tests.test_data import dataset_test_data


@patch("app.services.dataset.dataset_deletion_service.DeletionMetadataFirebaseRepository.mark_dataset_for_deletion")
@patch("app.services.dataset.dataset_deletion_service.DatasetDeletionService.process_collection_exercise_end_message")
@patch("app.services.dataset.dataset_deletion_service.DatasetService.get_dataset_metadata_collection")
@patch("app.services.dataset.dataset_deletion_service.DatasetDeletionService._collect_metadata_for_period_and_survey")
@patch("app.services.dataset.dataset_deletion_service.DatasetDeletionService._check_if_collection_has_dataset_guid")
def test_process_collection_exercise_end_message_through_endpoint(
        mock_check_dataset_guid, mock_collect_metadata, mock_get_dataset_metadat,
        mock_process_message, mock_mark_for_deletion, test_client):
    mock_check_dataset_guid.return_value = True
    mock_collect_metadata.return_value = dataset_test_data.dataset_metadata_collection_deletion
    mock_get_dataset_metadat.return_value = dataset_test_data.dataset_metadata_collection_deletion

    response = test_client.post(
        "/collection-exercise-end",
        json=dataset_test_data.test_data_collection_end_input,
    )

    assert response.status_code == 200

def test_check_if_collection_has_supplementary_data_return_true_when_dataset_id_present():
    dataset_delete_service = DatasetDeletionService()

    result = dataset_delete_service._check_if_collection_has_dataset_guid(
        dataset_test_data.test_data_collection_end
    )

    assert result

def test_check_if_collection_has_supplementary_data_return_false_when_dataset_id_not_present():
    dataset_delete_service = DatasetDeletionService()

    result = dataset_delete_service._check_if_collection_has_dataset_guid(
        dataset_test_data.test_data_collection_end_missing_id
    )

    assert not result

def test_collect_metadata_for_period_and_survey_returns_list_metadata():
    DatasetService.get_dataset_metadata_collection = MagicMock()
    DatasetService.get_dataset_metadata_collection.return_value = (
        dataset_test_data.dataset_metadata_collection_deletion
    )

    expected = [
        dataset_test_data.dataset_metadata_collection_deletion[0],
        dataset_test_data.dataset_metadata_collection_deletion[1],
    ]

    dataset_delete_service = DatasetDeletionService()

    result = dataset_delete_service._collect_metadata_for_period_and_survey(
        dataset_test_data.test_data_collection_end
    )

    assert result == expected

def test_mark_collections_for_deletion():
    DeletionMetadataFirebaseRepository.mark_dataset_for_deletion = MagicMock()

    dataset_delete_service = DatasetDeletionService()
    dataset_delete_service._mark_collections_for_deletion(
        dataset_test_data.dataset_metadata_collection_deletion
    )

    mark_for_deletion_called = (
        DeletionMetadataFirebaseRepository.mark_dataset_for_deletion.called
    )

    assert mark_for_deletion_called
