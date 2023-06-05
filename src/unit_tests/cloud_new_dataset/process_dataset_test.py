from unittest import TestCase
from unittest.mock import MagicMock, call

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.firestore_transaction_service import FirestoreTransactionService

from src.test_data import dataset_test_data, shared_test_data
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

        self.commit_transaction_stash = FirestoreTransactionService.commit_transaction
        self.rollback_transaction_stash = (
            FirestoreTransactionService.rollback_transaction
        )

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

        FirestoreTransactionService.commit_transaction = self.commit_transaction_stash
        FirestoreTransactionService.rollback_transaction = (
            self.rollback_transaction_stash
        )

    def test_upload_new_dataset(
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

        FirestoreTransactionService.commit_transaction = MagicMock()
        FirestoreTransactionService.rollback_transaction = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.assert_called_once_with(
            dataset_test_data.survey_id
        )
        DatasetFirebaseRepository.write_dataset_metadata_to_repository.assert_called_once_with(
            shared_test_data.test_guid,
            dataset_test_data.updated_dataset_metadata_without_id,
        )

        DatasetFirebaseRepository.get_dataset_unit_collection.assert_called_once_with(
            shared_test_data.test_guid
        )

        append_calls = [
            call(
                dataset_test_data.existing_dataset_unit_data_collection,
                dataset_test_data.dataset_unit_data_collection[0],
                dataset_test_data.dataset_unit_data_ruref[0],
            ),
            call(
                dataset_test_data.existing_dataset_unit_data_collection,
                dataset_test_data.dataset_unit_data_collection[1],
                dataset_test_data.dataset_unit_data_ruref[1],
            ),
        ]
        DatasetFirebaseRepository.append_unit_to_dataset_units_collection.assert_has_calls(
            append_calls
        )

    def test_delete_previous_versions_datasets_success(self):
        """
        Tests all previous versions of a dataset are deleted when a new dataset version is uploaded to firestore
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

        DatasetFirebaseRepository.delete_previous_versions_datasets = MagicMock()

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        FirestoreTransactionService.commit_transaction = MagicMock()
        FirestoreTransactionService.rollback_transaction = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.delete_previous_versions_datasets.assert_called_once_with(
            dataset_test_data.survey_id, dataset_test_data.new_dataset_version
        )

    def test_delete_previous_versions_datasets_failure(self):
        """
        Tests an exception is raised if there is an issue deleting previous dataset versions from firestore.
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

        DatasetFirebaseRepository.delete_previous_versions_datasets = MagicMock()
        DatasetFirebaseRepository.delete_previous_versions_datasets.side_effect = (
            Exception
        )

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        FirestoreTransactionService.commit_transaction = MagicMock()
        FirestoreTransactionService.rollback_transaction = MagicMock()

        with raises(
            RuntimeError,
            match="Failed to delete previous dataset versions from firestore.",
        ):
            TestHelper.new_dataset_mock(cloud_event)
