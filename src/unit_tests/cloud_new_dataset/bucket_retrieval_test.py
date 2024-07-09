from unittest import TestCase
from unittest.mock import MagicMock

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.dataset.dataset_processor_service import DatasetProcessorService

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class BucketRetrievalTest(TestCase):
    def setUp(self):
        self.fetch_first_filename_from_bucket_stash = DatasetBucketRepository.fetch_first_filename_from_bucket
        self.empty_bucket_stash = DatasetBucketRepository.delete_bucket_file
        self.process_raw_dataset_stash = DatasetProcessorService.process_raw_dataset

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetBucketRepository.fetch_first_filename_from_bucket = self.fetch_first_filename_from_bucket_stash
        DatasetBucketRepository.delete_bucket_file = self.empty_bucket_stash
        DatasetProcessorService.process_raw_dataset = self.process_raw_dataset_stash

    def test_empty_datasets_bucket_after_retrieval(self):
        """
        Tests datasets are deleted from the bucket after they have been retrieved.
        """
        #cloud_event = MagicMock()
        #cloud_event.data = dataset_test_data.cloud_event_data

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(return_value="test_filename.json")

        DatasetBucketRepository.delete_bucket_file = MagicMock()
        DatasetProcessorService.process_raw_dataset = MagicMock()

        TestHelper.new_dataset_mock(request=None)

        DatasetBucketRepository.delete_bucket_file.assert_called_once()

    def test_empty_datasets_bucket_failure(self):
        """
        Tests an exception is raised if there is an issue deleting data from the bucket.
        """
        #cloud_event = MagicMock()
        #cloud_event.data = dataset_test_data.cloud_event_data

        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(return_value="test_filename.json")

        DatasetBucketRepository.delete_bucket_file = MagicMock(side_effect=Exception)

        DatasetProcessorService.process_raw_dataset = MagicMock()

        with raises(
            RuntimeError,
            match="Failed to delete file from dataset bucket.",
        ):
            TestHelper.new_dataset_mock(request=None)

        DatasetBucketRepository.delete_bucket_file.reset_mock()
