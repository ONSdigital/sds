from logging_config import logging
from models.dataset_models import UnitDataset
from repositories.buckets.bucket_loader import BucketLoader
from repositories.buckets.bucket_repository import BucketRepository

logger = logging.getLogger(__name__)
bucket_loader = BucketLoader()


class DatasetBucketRepository(BucketRepository):
    def __init__(self):
        self.bucket = bucket_loader.get_dataset_bucket()

    def get_dataset_file_as_json(self, filename: str) -> UnitDataset:
        """
        Queries google bucket for file with a specific name and returns it as json.

        Parameters:
        filename (str): name of file being queried.

        Returns:
        RawDatasetWithMetadata: raw dataset from the bucket file as json.
        """
        return self.get_bucket_file_as_json(filename)
