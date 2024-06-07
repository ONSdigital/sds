from unittest import TestCase
from unittest.mock import MagicMock

from config.config_factory import config
from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.document_version_service import DocumentVersionService
from services.shared.publisher_service import PublisherService

from src.test_data import dataset_test_data, shared_test_data
from src.unit_tests.test_helper import TestHelper


class ProcessDatasetTest(TestCase):
    def setUp(self):
        self.get_latest_dataset_with_survey_id_stash = (
            DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id
        )
        self.perform_batched_dataset_write_stash = (
            DatasetFirebaseRepository.perform_batched_dataset_write
        )
        self.perform_delete_previous_version_dataset_transaction_stash = (
            DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction
        )
        self.calculate_previous_version_stash = (
            DocumentVersionService.calculate_previous_version
        )
        self.delete_bucket_file_stash = DatasetBucketRepository.delete_bucket_file
        self.publish_data_to_topic_stash = PublisherService.publish_data_to_topic
        self.config_retain_dataset_firestore_stash = config.RETAIN_DATASET_FIRESTORE

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            self.get_latest_dataset_with_survey_id_stash
        )
        DatasetFirebaseRepository.perform_batched_dataset_write = (
            self.perform_batched_dataset_write_stash
        )
        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            self.perform_delete_previous_version_dataset_transaction_stash
        )
        DocumentVersionService.calculate_previous_version = (
            self.calculate_previous_version_stash
        )
        DatasetBucketRepository.delete_bucket_file = self.delete_bucket_file_stash
        PublisherService.publish_data_to_topic = self.publish_data_to_topic_stash
        config.RETAIN_DATASET_FIRESTORE = self.config_retain_dataset_firestore_stash

    def test_upload_new_dataset_first_version(
        self,
    ):
        """
        The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=None)
        )
        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()
        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id.assert_called_once_with(
            dataset_test_data.survey_id, dataset_test_data.period_id
        )

        DatasetFirebaseRepository.perform_batched_dataset_write.assert_called_once_with(
            shared_test_data.test_guid,
            dataset_test_data.first_dataset_metadata_without_id,
            dataset_test_data.dataset_unit_data_collection,
            dataset_test_data.dataset_unit_data_identifier,
        )

    def test_upload_new_dataset_updated_version(
        self,
    ):
        """
        The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=dataset_test_data.dataset_metadata_first_version)
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id.assert_called_once_with(
            dataset_test_data.survey_id, dataset_test_data.period_id
        )

        DatasetFirebaseRepository.perform_batched_dataset_write.assert_called_once_with(
            shared_test_data.test_guid,
            dataset_test_data.updated_dataset_metadata_without_id,
            dataset_test_data.dataset_unit_data_collection,
            dataset_test_data.dataset_unit_data_identifier,
        )

    def test_perform_delete_previous_version_dataset_transaction_success(self):
        """
        Tests the previous version of dataset are deleted when a new dataset version is uploaded to firestore.

        This test simulates a successful dataset upload process when retain flag is off. It assert
        the deletion process will be run with appropriate arguments
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data
        config.RETAIN_DATASET_FIRESTORE = False

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=(dataset_test_data.dataset_metadata_first_version))
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        DocumentVersionService.calculate_previous_version = MagicMock()
        DocumentVersionService.calculate_previous_version.return_value = 1

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction.assert_called_once_with(
            dataset_test_data.survey_id,
            dataset_test_data.period_id,
            dataset_test_data.updated_dataset_version - 1,
        )

    def test_perform_delete_previous_version_dataset_transaction_failure(self):
        """
        Tests an exception is raised if there is an issue deleting previous dataset versions from firestore.

        This test simulates an exception raising in the dataset deletion process. It assert
        the appropriate runtime error will be prompted when it happens to ensure the rollback process.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data
        config.RETAIN_DATASET_FIRESTORE = False

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=(dataset_test_data.dataset_metadata_first_version))
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = MagicMock(
            side_effect=Exception
        )

        DatasetBucketRepository.delete_bucket_file = MagicMock()

        DocumentVersionService.calculate_previous_version = MagicMock()
        DocumentVersionService.calculate_previous_version.return_value = 1

        with raises(
            RuntimeError,
            match="Failed to delete previous version of dataset from firestore. Rolling back...",
        ):
            TestHelper.new_dataset_mock(cloud_event)

    def test_skip_perform_delete_previous_version_dataset_when_retention_flag_is_on(
        self,
    ):
        """
        Tests the deletion process is skipped when retention flag is on.

        This test simulates the upload of an updated version of datset when retain flag is on.
        The test assert that no deletion process will be attempted.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data
        config.RETAIN_DATASET_FIRESTORE = True

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=(dataset_test_data.dataset_metadata_first_version))
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        DocumentVersionService.calculate_previous_version = MagicMock()
        DocumentVersionService.calculate_previous_version.return_value = 1

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction.assert_not_called()

    def test_skip_perform_delete_previous_version_dataset_when_dataset_first_upload(
        self,
    ):
        """
        Tests the deletion process is skipped when a dataset is uploaded the first time.

        This test simulates the upload of the first version of dataset and assert that
        no deletion process will be attempted even when retain flag is off.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data
        config.RETAIN_DATASET_FIRESTORE = False

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=None)
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        DocumentVersionService.calculate_previous_version = MagicMock()
        DocumentVersionService.calculate_previous_version.return_value = 0

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction.assert_not_called()

    def test_skip_perform_delete_previous_version_dataset_when_dataset_upload_failed(
        self,
    ):
        """
        Tests the deletion process is skipped when new uploaded dataset is not found in database.

        This test simulates the upload of dataset while a version 2 of the dataset exists
        After the upload process, the calculation of previous dataset version is mocked to return
        a non-incremented version (1 instead of 2) simulating a failed upload in transaction
        The test then assert the data deletion process will not run even when retain flag is off.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data
        config.RETAIN_DATASET_FIRESTORE = False

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=(dataset_test_data.dataset_metadata_updated_version))
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        DocumentVersionService.calculate_previous_version = MagicMock()
        DocumentVersionService.calculate_previous_version.return_value = 1

        TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction.assert_not_called()

    def test_runtime_error_in_calculate_previous_version_of_dataset_when_dataset_not_found(
        self,
    ):
        """
        Tests appropriate runtime error will be promted when dataset is not found during
        previous version calculation.

        This test turn off the retain flag and mock the return of latest dataset to None
        to simulate a dataset not found situation. The test then assert the runtime error
        and check the deletion is not processed.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data
        config.RETAIN_DATASET_FIRESTORE = False

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock(return_value=None)
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        with raises(
            RuntimeError,
            match="Current version document is not found in calculate previous version service",
        ):
            TestHelper.new_dataset_mock(cloud_event)

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_transaction.assert_not_called()
