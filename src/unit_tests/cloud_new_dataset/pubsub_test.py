from unittest import TestCase
from unittest.mock import MagicMock

from config.config_factory import config
from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.publisher_service import PublisherService

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class PubSubTest(TestCase):
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

    def test_dataset_transaction_success_publish_response(self):
        """
        When the dataset transaction is successful a success response should be published to the datset topic
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock(
                [dataset_test_data.dataset_metadata]
            )
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        PublisherService.publish_data_to_topic.assert_called_once_with(
            dataset_test_data.updated_dataset_metadata, config.PUBLISH_DATASET_TOPIC_ID
        )

    def test_dataset_transaction_fail_publish_response(
        self,
    ):
        """
        When the dataset transaction fails a failure response should be published to the datset topic
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock(
                [dataset_test_data.dataset_metadata]
            )
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock(
            side_effect=Exception
        )

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        PublisherService.publish_data_to_topic.assert_called_once_with(
            {"status": "error", "message": "Publishing dataset has failed."},
            config.PUBLISH_DATASET_TOPIC_ID,
        )

    def test_dataset_metadata_transaction_fail_publish_response(
        self,
    ):
        """
        When there is an issue with the dataset data publishing an error should be raised
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
            TestHelper.create_document_snapshot_generator_mock(
                [dataset_test_data.dataset_metadata]
            )
        )

        DatasetFirebaseRepository.perform_new_dataset_transaction = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock(side_effect=Exception)

        DatasetFirebaseRepository.perform_delete_previous_versions_datasets_transaction = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        with raises(
            RuntimeError, match="Error publishing dataset response to the topic."
        ):
            TestHelper.new_dataset_mock(cloud_event)
