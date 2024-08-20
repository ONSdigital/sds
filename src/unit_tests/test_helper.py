import json
from unittest.mock import MagicMock

from config.config_factory import config
from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository


class TestHelper:
    @staticmethod
    def new_dataset_mock(request):
        """
        Mocks the cloud function call.
        """
        from main import new_dataset

        return new_dataset(request)

    @staticmethod
    def mock_get_dataset_from_bucket():
        """
        Mocks the application's google bucket boundaries.
        """
        with open(f"{config.TEST_DATASET_PATH}/dataset.json") as f:
            dataset_with_metadata: UnitDataset = json.load(f)

        DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json.return_value = (
            dataset_with_metadata
        )
