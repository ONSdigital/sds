# import uuid
# from unittest import TestCase
# from unittest.mock import MagicMock
#
# import pytest
# from repositories.firebase.deletion_firebase_repository import (
#     DeletionMetadataFirebaseRepository,
# )
# from services.dataset.dataset_deletion_service import DatasetDeletionService
# from services.dataset.dataset_processor_service import DatasetProcessorService
#
# from repositories.firebase.dataset_firebase_repository import (
#     DatasetFirebaseRepository,
# )
# from src.test_data import dataset_test_data
#
#
#
#
# class PostSchemaTest(TestCase):
#
#     @pytest.fixture(autouse=True)
#     def prepare_fixture(self, test_client):
#         self.test_client = test_client
#
#     # def test_process_collection_exercise_end_message(self):
#     #     DatasetProcessorService.get_dataset_metadata_collection = MagicMock()
#     #     DatasetProcessorService.get_dataset_metadata_collection.return_value = (
#     #         dataset_test_data.dataset_metadata_collection_deletion
#     #     )
#     #
#     #     DatasetFirebaseRepository.get_dataset_metadata_collection = MagicMock()
#     #     DatasetFirebaseRepository.get_dataset_metadata_collection.return_value = (
#     #         dataset_test_data.dataset_metadata_collection_deletion
#     #     )
#     #
#     #     DeletionMetadataFirebaseRepository.mark_dataset_for_deletion = MagicMock()
#     #
#     #     DatasetDeletionService.process_collection_exercise_end_message = MagicMock()
#     #
#     #     collection_exercise_end = {
#     #         "dataset_guid": uuid.uuid4(),
#     #         "period_id": "period_id",
#     #         "survey_id": "survey_id",
#     #     }
#     #
#     #     response = self.test_client.post(
#     #         "/collection-exercise-end", json=collection_exercise_end
#     #     )
#     #     assert response.status_code == 200
#
#     def test_check_if_collection_has_supplementary_data_return_true_when_dataset_id_present(
#         self,
#     ):
#         dataset_delete_service = DatasetDeletionService()
#
#         result = dataset_delete_service._check_if_collection_has_supplementary_data(
#             dataset_test_data.test_data_collection_end
#         )
#
#         assert result == True
#
#     def test_check_if_collection_has_supplementary_data_return_false_when_dataset_id_not_present(
#         self,
#     ):
#         dataset_delete_service = DatasetDeletionService()
#
#         result = dataset_delete_service._check_if_collection_has_supplementary_data(dataset_test_data.test_data_collection_end_missing_id)
#
#         assert result == False
#
#     def test_collect_metadata_for_period_and_survey_returns_list_metadata(self):
#         DatasetProcessorService.get_dataset_metadata_collection = MagicMock()
#         DatasetProcessorService.get_dataset_metadata_collection.return_value = (
#             dataset_test_data.dataset_metadata_collection_deletion
#         )
#
#         DatasetFirebaseRepository.get_dataset_metadata_collection = MagicMock()
#         DatasetFirebaseRepository.get_dataset_metadata_collection.return_value = (
#             dataset_test_data.dataset_metadata_collection_deletion
#         )
#
#         expected = [
#             {
#                 **dataset_test_data.dataset_metadata_collection_deletion[0],
#             },
#             {
#                 **dataset_test_data.dataset_metadata_collection_deletion[1],
#             },
#         ]
#
#         dataset_delete_service = DatasetDeletionService()
#
#         result = dataset_delete_service._collect_metadata_for_period_and_survey(
#             dataset_test_data.test_data_collection_end
#         )
#
#         assert result == expected
#
#     def test_mark_collections_for_deletion(self):
#         DeletionMetadataFirebaseRepository.mark_dataset_for_deletion = MagicMock()
#         DeletionMetadataFirebaseRepository.mark_dataset_for_deletion.called
#
#         dataset_delete_service = DatasetDeletionService()
#         dataset_delete_service._mark_collections_for_deletion(
#             dataset_test_data.dataset_metadata_collection_deletion
#         )
