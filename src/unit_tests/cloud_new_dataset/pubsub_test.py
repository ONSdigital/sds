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
        self.fetch_first_filename_from_bucket_stash = (
            DatasetBucketRepository.fetch_first_filename_from_bucket
        )
        self.get_latest_dataset_with_survey_id_stash = (
            DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id
        )
        self.perform_batched_dataset_write_stash = (
            DatasetFirebaseRepository.perform_batched_dataset_write
        )
        self.perform_delete_previous_version_dataset_batch_stash = (
            DatasetFirebaseRepository.perform_delete_previous_version_dataset_batch
        )
        self.get_number_of_unit_supplementary_data_with_dataset_id_stash = (
            DatasetFirebaseRepository.get_number_of_unit_supplementary_data_with_dataset_id
        )
        self.delete_bucket_file_stash = DatasetBucketRepository.delete_bucket_file
        self.publish_data_to_topic_stash = PublisherService.publish_data_to_topic

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetBucketRepository.fetch_first_filename_from_bucket = (
            self.fetch_first_filename_from_bucket_stash
        )
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            self.get_latest_dataset_with_survey_id_stash
        )
        DatasetFirebaseRepository.perform_batched_dataset_write = (
            self.perform_batched_dataset_write_stash
        )
        DatasetFirebaseRepository.get_number_of_unit_supplementary_data_with_dataset_id = (
            self.get_number_of_unit_supplementary_data_with_dataset_id_stash
        )
        DatasetFirebaseRepository.perform_delete_previous_version_dataset_batch = (
            self.perform_delete_previous_version_dataset_batch_stash
        )
        DatasetBucketRepository.delete_bucket_file = self.delete_bucket_file_stash
        PublisherService.publish_data_to_topic = self.publish_data_to_topic_stash

    def test_dataset_batch_write_success_publish_response(self):
        """
        When the dataset batch write is successful a success response should be published to the dataset topic
        """

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(return_value="test_filename.json")

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock()
        )
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id.return_value = (
            dataset_test_data.dataset_metadata_first_version
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        DatasetFirebaseRepository.get_number_of_unit_supplementary_data_with_dataset_id = MagicMock(
            return_value=2
        )

        PublisherService.publish_data_to_topic = MagicMock()

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_batch = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        TestHelper.new_dataset_mock(request=None)

        PublisherService.publish_data_to_topic.assert_called_once_with(
            dataset_test_data.updated_dataset_metadata, config.PUBLISH_DATASET_TOPIC_ID
        )

    def test_dataset_metadata_fail_publish_response(
        self,
    ):
        """
        When there is an issue with the dataset data publishing an error should be raised
        """

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(return_value="test_filename.json")

        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id = (
            MagicMock()
        )
        DatasetFirebaseRepository.get_latest_dataset_with_survey_id_and_period_id.return_value = (
            dataset_test_data.dataset_metadata_first_version
        )

        DatasetFirebaseRepository.perform_batched_dataset_write = MagicMock()

        DatasetFirebaseRepository.get_number_of_unit_supplementary_data_with_dataset_id = MagicMock(
            return_value=2
        )

        PublisherService.publish_data_to_topic = MagicMock()

        PublisherService.publish_data_to_topic = MagicMock(side_effect=Exception)

        DatasetFirebaseRepository.perform_delete_previous_version_dataset_batch = (
            MagicMock()
        )
        DatasetBucketRepository.delete_bucket_file = MagicMock()

        with raises(
            RuntimeError, match="Error publishing dataset response to the topic."
        ):
            TestHelper.new_dataset_mock(request=None)
