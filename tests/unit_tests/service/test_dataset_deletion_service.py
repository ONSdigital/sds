from unittest import TestCase
from unittest.mock import MagicMock

import pytest
from app.repositories.firebase.deletion_firebase_repository import (
    DeletionMetadataFirebaseRepository,
)
from app.services.dataset.dataset_deletion_service import DatasetDeletionService
from app.services.dataset.dataset_service import DatasetService

from tests.test_data import dataset_test_data


class PostSchemaTest(TestCase):

    @pytest.fixture(autouse=True)
    def prepare_fixture(self, test_client):
        self.test_client = test_client

    def test_process_collection_exercise_end_message_through_endpoint(self):
        DatasetDeletionService.process_collection_exercise_end_message = MagicMock()

        DatasetDeletionService._check_if_collection_has_dataset_guid = MagicMock()
        DatasetDeletionService._check_if_collection_has_dataset_guid.return_value(
            True
        )

        DatasetDeletionService._collect_metadata_for_period_and_survey = MagicMock()
        DatasetDeletionService._collect_metadata_for_period_and_survey.return_value = (
            dataset_test_data.dataset_metadata_collection_deletion
        )

        DatasetService.get_dataset_metadata_collection = MagicMock()
        DatasetService.get_dataset_metadata_collection.return_value = (
            dataset_test_data.dataset_metadata_collection_deletion
        )

        DeletionMetadataFirebaseRepository.mark_dataset_for_deletion = MagicMock()

        DatasetDeletionService.process_collection_exercise_end_message = MagicMock()

        response = self.test_client.post(
            "/collection-exercise-end",
            json=dataset_test_data.test_data_collection_end_input,
        )

        assert response.status_code == 200

    def test_check_if_collection_has_supplementary_data_return_true_when_dataset_id_present(
        self,
    ):
        dataset_delete_service = DatasetDeletionService()

        result = dataset_delete_service._check_if_collection_has_dataset_guid(
            dataset_test_data.test_data_collection_end
        )

        assert result

    def test_check_if_collection_has_supplementary_data_return_false_when_dataset_id_not_present(
        self,
    ):
        dataset_delete_service = DatasetDeletionService()

        result = dataset_delete_service._check_if_collection_has_dataset_guid(
            dataset_test_data.test_data_collection_end_missing_id
        )

        assert not result

    def test_collect_metadata_for_period_and_survey_returns_list_metadata(self):
        DatasetService.get_dataset_metadata_collection = MagicMock()
        DatasetService.get_dataset_metadata_collection.return_value = (
            dataset_test_data.dataset_metadata_collection_deletion
        )

        expected = [
            {
                **dataset_test_data.dataset_metadata_collection_deletion[0],
            },
            {
                **dataset_test_data.dataset_metadata_collection_deletion[1],
            },
        ]

        dataset_delete_service = DatasetDeletionService()

        result = dataset_delete_service._collect_metadata_for_period_and_survey(
            dataset_test_data.test_data_collection_end
        )

        assert result == expected

    def test_mark_collections_for_deletion(self):
        DeletionMetadataFirebaseRepository.mark_dataset_for_deletion = MagicMock()

        dataset_delete_service = DatasetDeletionService()
        dataset_delete_service._mark_collections_for_deletion(
            dataset_test_data.dataset_metadata_collection_deletion
        )

        mark_for_deletion_called = (
            DeletionMetadataFirebaseRepository.mark_dataset_for_deletion.called
        )

        assert mark_for_deletion_called
