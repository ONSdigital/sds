from logging_config import logging
from models.dataset_models import UnitDataset
from repositories.buckets.bucket_loader import BucketLoader
from repositories.buckets.bucket_repository import BucketRepository

logger = logging.getLogger(__name__)


class DatasetBucketRepository(BucketRepository):
    def __init__(self, bucket_name: str):
        bucket_loader = BucketLoader()
        self.bucket = bucket_loader.get_dataset_bucket(bucket_name)

    def get_dataset_file_as_json(self, filename: str) -> UnitDataset:
        """
        Queries google bucket for file with a specific name and returns it as json.

        Parameters:
        filename (str): name of file being queried.

        Returns:
        RawDatasetWithMetadata: raw dataset from the bucket file as json.
        """
        return self.get_bucket_file_as_json(filename)
