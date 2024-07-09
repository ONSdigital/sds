import re

from unittest import TestCase
from unittest.mock import MagicMock
from pytest import raises

from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.dataset.dataset_bucket_service import DatasetBucketService

from src.unit_tests.test_helper import TestHelper


class FetchDatasetTest(TestCase):
    def setUp(self):
        self.fetch_first_filename_from_bucket_stash = (
            DatasetBucketRepository.fetch_first_filename_from_bucket
        )
        self.get_and_validate_dataset_stash = DatasetBucketService.get_and_validate_dataset
        self.fetch_first_filename_from_bucket_stash = DatasetBucketRepository.fetch_first_filename_from_bucket

        TestHelper.mock_get_dataset_from_bucket()

    def tearDown(self):
        DatasetBucketRepository.fetch_first_filename_from_bucket = (
            self.fetch_first_filename_from_bucket_stash
        )
        DatasetBucketService.get_and_validate_dataset = self.get_and_validate_dataset_stash
        DatasetBucketRepository.fetch_first_filename_from_bucket = self.fetch_first_filename_from_bucket_stash

    def test_fetch_no_dataset_from_bucket(
        self,
    ):
        """
        When there is no dataset in the bucket, an error should be raised
        """
        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(return_value=None)
        DatasetBucketService.get_and_validate_dataset = MagicMock()

        result = TestHelper.new_dataset_mock(request=None)

        assert result == ('{"success": true}', 200, {'ContentType': 'application/json'})
        DatasetBucketService.get_and_validate_dataset.assert_not_called()

    def test_fetch_dataset_from_bucket_failed(
            self,
    ):
        """
        When the dataset fetch from the bucket fails, an error should be raised
        """
        DatasetBucketRepository.fetch_first_filename_from_bucket = MagicMock(side_effect=Exception)

        with raises(
            RuntimeError,
            match=re.escape("Failed to fetch first filename from dataset bucket."),
        ):
            TestHelper.new_dataset_mock(request=None)