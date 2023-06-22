from unittest import TestCase
from unittest.mock import MagicMock

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class ProcessDatasetTest(TestCase):
    def setUp(self):
        self.get_latest_dataset_with_survey_id_stash = (
            DatasetFirebaseRepository.get_latest_dataset_with_survey_id
        )
        self.perform_new_dataset_transaction_stash = (
            DatasetFirebaseRepository.perform_new_dataset_transaction
        )
        self.perform_delete_previous_versions_datasets_transaction_stash = (
            DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction
        )
        self.delete_bucket_file_stash = DatasetBucketRepository.delete_bucket_file

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = (
            self.get_latest_dataset_with_survey_id_stash
        )
        DatasetFirebaseRepository.perform_new_dataset_transaction = (
            self.perform_new_dataset_transaction_stash
        )
        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            self.perform_delete_previous_versions_datasets_transaction_stash
        )
        DatasetBucketRepository.delete_bucket_file = self.delete_bucket_file_stash

    def test_transaction_rolled_back_on_metadata_write_failure(
        self,
    ):
        """
        Testing the first transaction action, writing metadata, causes the transaction to rollback if it fails.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
            dataset_test_data.dataset_metadata
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()
        DatasetFirebaseRepository.perform_new_dataset_transaction.side_effect = (
            Exception
        )

        DatasetBucketRepository.delete_bucket_file = MagicMock()
        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )

        with raises(
            Exception,
            match="Error performing dataset transaction.",
        ):
            TestHelper.new_dataset_mock(cloud_event)
