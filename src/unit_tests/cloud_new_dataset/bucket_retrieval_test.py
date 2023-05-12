from unittest import TestCase
from unittest.mock import MagicMock

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.dataset.dataset_processor_service import DatasetProcessorService

from src.test_data import dataset_test_data
from src.unit_tests.test_helper import TestHelper


class BucketRetrievalTest(TestCase):
    def setUp(self):
        self.empty_bucket_stash = DatasetBucketRepository.empty_bucket
        self.process_raw_dataset_stash = DatasetProcessorService.process_raw_dataset

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetBucketRepository.empty_bucket = self.empty_bucket_stash
        DatasetProcessorService.process_raw_dataset = self.process_raw_dataset_stash

    def test_empty_datasets_bucket_after_retrieval(self):
        """
        Tests datasets are deleted from the bucket after they have been retrieved.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetBucketRepository.empty_bucket = MagicMock()
        DatasetProcessorService.process_raw_dataset = MagicMock()

        TestHelper.new_dataset_mock(cloud_event)

        DatasetBucketRepository.empty_bucket.assert_called_once()

    def test_empty_datasets_bucket_failure(self):
        """
        Tests an exception is raised if there is an issue deleting data from the bucket.
        """
        cloud_event = MagicMock()
        cloud_event.data = dataset_test_data.cloud_event_data

        DatasetBucketRepository.empty_bucket = MagicMock()
        DatasetBucketRepository.empty_bucket.side_effect = Exception

        DatasetProcessorService.process_raw_dataset = MagicMock()

        with raises(
            RuntimeError,
            match="Failed to empty dataset bucket.",
        ):
            TestHelper.new_dataset_mock(cloud_event)

        DatasetBucketRepository.empty_bucket.reset_mock()
