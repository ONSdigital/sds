from google.cloud import storage
from logging_config import logging
from models.dataset_models import RawDatasetWithMetadata
from services.shared.bucket_operations_service import BucketOperationsService

logger = logging.getLogger(__name__)


class DatasetBucketRepository:
    def __init__(self, bucket_name: str):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def get_bucket_file_as_json(self, filename: str) -> RawDatasetWithMetadata:
        """Used by the cloud function."""
        return BucketOperationsService.get_bucket_file_as_json(filename, self.bucket)
