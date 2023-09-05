import json
from unittest.mock import MagicMock

from config.config_factory import config
from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository


class TestHelper:
    @staticmethod
    def new_dataset_mock(cloud_event):
        """
        Mocks the cloud function call.
        """
        from main import new_dataset

        return new_dataset(cloud_event)

    @staticmethod
    def mock_get_dataset_from_bucket():
        """
        Mocks the application's google bucket boundaries.
        """
        with open(config.TEST_DATASET_PATH) as f:
            dataset_with_metadata: UnitDataset = json.load(f)

        DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json.return_value = (
            dataset_with_metadata
        )
