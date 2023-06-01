from unittest import TestCase
from unittest.mock import MagicMock
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class ProcessDatasetTest(TestCase):
    def setUp(self):
        self.get_latest_dataset_with_survey_id_stash = (
            DatasetFirebaseRepository.get_latest_dataset_with_survey_id
        )
        self.write_dataset_metadata_to_repository_stash = (
            DatasetFirebaseRepository.write_dataset_metadata_to_repository
        )
        self.get_dataset_unit_collection_stash = (
            DatasetFirebaseRepository.get_dataset_unit_collection
        )
        self.append_unit_to_dataset_units_collection_stash = (
            DatasetFirebaseRepository.append_unit_to_dataset_units_collection
        )
        self.delete_previous_versions_datasets_stash = (
            DatasetFirebaseRepository.delete_previous_versions_datasets
        )
        self.delete_bucket_file_stash = DatasetBucketRepository.delete_bucket_file

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = (
            self.get_latest_dataset_with_survey_id_stash
        )
        DatasetFirebaseRepository.write_dataset_metadata_to_repository = (
            self.write_dataset_metadata_to_repository_stash
        )
        DatasetFirebaseRepository.get_dataset_unit_collection = (
            self.get_dataset_unit_collection_stash
        )
        DatasetFirebaseRepository.append_unit_to_dataset_units_collection = (
            self.append_unit_to_dataset_units_collection_stash
        )
        DatasetFirebaseRepository.delete_previous_versions_datasets = (
            self.delete_previous_versions_datasets_stash
        )
        DatasetBucketRepository.delete_bucket_file = self.delete_bucket_file_stash

    def test_transaction_rolled_back_on_metadata_write_failure(
        self,
    ):
        """
        The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock(
                [dataset_test_data.dataset_metadata]
            )
        )

        DatasetFirebaseRepository.write_dataset_metadata_to_repository = MagicMock()

        DatasetFirebaseRepository.get_dataset_unit_collection = MagicMock()
        DatasetFirebaseRepository.get_dataset_unit_collection.return_value = (
            dataset_test_data.existing_dataset_unit_data_collection
        )

        DatasetFirebaseRepository.append_unit_to_dataset_units_collection = MagicMock()

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        DatasetFirebaseRepository.delete_previous_versions_datasets = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)
