import re
from json import JSONDecodeError
from unittest import TestCase
from unittest.mock import MagicMock

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.dataset.dataset_bucket_service import DatasetBucketService
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.validators.dataset_validator_service import DatasetValidatorService

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class DatasetValidationTest(TestCase):
    def setUp(self):
        self.fetch_first_filename_from_bucket_stash = (
            DatasetBucketRepository.fetch_first_filename_from_bucket
        )
        self.try_delete_bucket_file_stash = DatasetBucketService.try_delete_bucket_file
        self.process_raw_dataset_stash = DatasetProcessorService.process_raw_dataset
        self.get_dataset_file_as_json_stash = (
            DatasetBucketRepository.get_dataset_file_as_json
        )
        self.publish_dataset_error_to_topic_stash = (
            DatasetValidatorService.try_publish_dataset_error_to_topic
        )

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetBucketRepository.fetch_first_filename_from_bucket = (
            self.fetch_first_filename_from_bucket_stash
        )
        DatasetBucketService.try_delete_bucket_file = self.try_delete_bucket_file_stash
        DatasetProcessorService.process_raw_dataset = self.process_raw_dataset_stash
        DatasetBucketRepository.get_dataset_file_as_json = (
            self.get_dataset_file_as_json_stash
        )
        DatasetValidatorService.try_publish_dataset_error_to_topic = (
            self.publish_dataset_error_to_topic_stash
        )

    def test_upload_invalid_file_type(self):
        """
        Tests the validation for when the file extension is not a json
        """
        # cloud_event = MagicMock()
        # cloud_event.data = dataset_test_data.cloud_event_invalid_filename_data

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(
            return_value="bad_filename.test"
        )

        DatasetBucketService.try_delete_bucket_file = MagicMock()
        DatasetProcessorService.process_raw_dataset = MagicMock()
        DatasetValidatorService.try_publish_dataset_error_to_topic = MagicMock()

        with raises(
            RuntimeError,
            match=f"Invalid filetype received.",
        ):
            TestHelper.new_dataset_mock(request=None)

        DatasetProcessorService.process_raw_dataset.assert_not_called()

    def test_no_dataset_in_bucket(self):
        """
        Validates when an empty object is returned from the bucket.
        """

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(
            return_value="test_filename.json"
        )

        DatasetBucketService.try_delete_bucket_file = MagicMock()
        DatasetProcessorService.process_raw_dataset = MagicMock()

        DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json.return_value = None

        with raises(
            RuntimeError,
            match="No corresponding dataset found in bucket",
        ):
            TestHelper.new_dataset_mock(request=None)

        DatasetProcessorService.process_raw_dataset.assert_not_called()

    def test_missing_dataset_keys(self):
        """
        Validates when there are mandatory keys missing from the dataset.
        """

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(
            return_value="test_filename.json"
        )

        DatasetBucketService.try_delete_bucket_file = MagicMock()
        DatasetProcessorService.process_raw_dataset = MagicMock()

        DatasetBucketRepository.get_dataset_file_as_json.return_value = (
            dataset_test_data.missing_keys_dataset_metadata
        )
        DatasetValidatorService.try_publish_dataset_error_to_topic = MagicMock()

        with raises(
            RuntimeError,
            match=re.escape("Mandatory key(s) missing from JSON: survey_id."),
        ):
            TestHelper.new_dataset_mock(request=None)

        DatasetProcessorService.process_raw_dataset.assert_not_called()

    def test_invalid_json_content(self):
        """
        Validates when the content of the dataset is not valid JSON.
        """

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(
            return_value="test_filename.json"
        )

        DatasetBucketService.try_delete_bucket_file = MagicMock()
        DatasetProcessorService.process_raw_dataset = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json = MagicMock(
            side_effect=JSONDecodeError("Expecting value", "", 0)
        )
        DatasetValidatorService.try_publish_dataset_error_to_topic = MagicMock()

        with raises(
            RuntimeError,
            match=re.escape("Invalid JSON content received."),
        ):
            TestHelper.new_dataset_mock(request=None)

        DatasetProcessorService.process_raw_dataset.assert_not_called()
