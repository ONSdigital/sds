import re
from json import JSONDecodeError
from unittest import TestCase
from unittest.mock import MagicMock

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.validators.dataset_validator_service import DatasetValidatorService

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class DatasetValidationTest(TestCase):
    def setUp(self):
        self.process_raw_dataset_stash = DatasetProcessorService.process_raw_dataset
        self.get_dataset_file_as_json_stash = (
            DatasetBucketRepository.get_dataset_file_as_json
        )
        self.publish_dataset_error_to_topic_stash = (
            DatasetValidatorService._publish_dataset_error_to_topic
        )

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetProcessorService.process_raw_dataset = self.process_raw_dataset_stash
        DatasetBucketRepository.get_dataset_file_as_json = (
            self.get_dataset_file_as_json_stash
        )
        DatasetValidatorService._publish_dataset_error_to_topic = (
            self.publish_dataset_error_to_topic_stash
        )

    def test_upload_invalid_file_type(self):
        """
        Tests the validation for when the file extension is not a json
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_invalid_filename_data

        DatasetProcessorService.process_raw_dataset = MagicMock()
        DatasetValidatorService._publish_dataset_error_to_topic = MagicMock()

        with raises(
            RuntimeError,
            match=f"Invalid filetype received - {dataset_test_data.cloud_event_invalid_filename_data['name']}",
        ):
            TestHelper.new_dataset_mock(cloud_event)

        DatasetProcessorService.process_raw_dataset.assert_not_called()

    def test_no_dataset_in_bucket(self):
        """
        Validates when an empty object is returned from the bucket.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetProcessorService.process_raw_dataset = MagicMock()

        DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json.return_value = None

        with raises(
            RuntimeError,
            match="No corresponding dataset found in bucket",
        ):
            TestHelper.new_dataset_mock(cloud_event)

        DatasetProcessorService.process_raw_dataset.assert_not_called()

    def test_missing_dataset_keys(self):
        """
        Validates when there are mandatory keys missing from the dataset.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetProcessorService.process_raw_dataset = MagicMock()

        DatasetBucketRepository.get_dataset_file_as_json.return_value = (
            dataset_test_data.missing_keys_dataset_metadata
        )
        DatasetValidatorService._publish_dataset_error_to_topic = MagicMock()

        with raises(
            RuntimeError,
            match=re.escape("Mandatory key(s) missing from JSON: survey_id."),
        ):
            TestHelper.new_dataset_mock(cloud_event)

        DatasetProcessorService.process_raw_dataset.assert_not_called()

    def test_invalid_json_content(self):
        """
        Validates when the content of the dataset is not valid JSON.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetProcessorService.process_raw_dataset = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json = MagicMock(
            side_effect=JSONDecodeError("Expecting value", "", 0)
        )
        DatasetValidatorService._publish_dataset_error_to_topic = MagicMock()

        with raises(
            RuntimeError,
            match=re.escape("Invalid JSON content received."),
        ):
            TestHelper.new_dataset_mock(cloud_event)

        DatasetProcessorService.process_raw_dataset.assert_not_called()
