from unittest import TestCase
from unittest.mock import MagicMock

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.publisher_service import PublisherService

from src.test_data import dataset_test_data, shared_test_data
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
        self.publish_data_to_topic_stash = PublisherService.publish_data_to_topic

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
        PublisherService.publish_data_to_topic = self.publish_data_to_topic_stash

    def test_upload_new_dataset_first_version(
        self,
    ):
        """
        The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock(
            return_value=None
        )
        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()
        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.assert_called_once_with(
            dataset_test_data.survey_id
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction.assert_called_once_with(
            shared_test_data.test_guid,
            dataset_test_data.first_dataset_metadata_without_id,
            dataset_test_data.dataset_unit_data_collection,
            dataset_test_data.dataset_unit_data_ruref,
        )

    def test_upload_new_dataset_updated_version(
        self,
    ):
        """
        The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock(
            return_value=dataset_test_data.dataset_metadata_first_version
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.assert_called_once_with(
            dataset_test_data.survey_id
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction.assert_called_once_with(
            shared_test_data.test_guid,
            dataset_test_data.updated_dataset_metadata_without_id,
            dataset_test_data.dataset_unit_data_collection,
            dataset_test_data.dataset_unit_data_ruref,
        )

    def test_perform_delete_previous_versions_datasets_transaction_success(self):
        """
        Tests all previous versions of a dataset are deleted when a new dataset version is uploaded to firestore
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock(
            return_value=(dataset_test_data.dataset_metadata_first_version)
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction.assert_called_once_with(
            dataset_test_data.survey_id, dataset_test_data.updated_dataset_version
        )

    def test_perform_delete_previous_versions_datasets_transaction_failure(self):
        """
        Tests an exception is raised if there is an issue deleting previous dataset versions from firestore.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock(
            return_value=(dataset_test_data.dataset_metadata_first_version)
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = MagicMock(
            side_effect=Exception
        )

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        with raises(
            RuntimeError,
            match="Failed to delete previous dataset versions from firestore. Rolling back...",
        ):
            TestHelper.new_dataset_mock(cloud_event)
