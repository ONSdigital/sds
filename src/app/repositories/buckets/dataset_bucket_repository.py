from google.cloud import storage
from logging_config import logging
from models.dataset_models import RawDatasetWithMetadata
from services.shared.bucket_operations_service import BucketOperationsService

logger = logging.getLogger(__name__)


class DatasetBucketRepository:
    def __init__(self):
        self.storage_client = storage.Client()

    def get_file_from_bucket(
        self, filename: str, bucket_name: str
    ) -> RawDatasetWithMetadata:
        """Used by the cloud function."""
        bucket = self.storage_client.bucket(bucket_name)

        return BucketOperationsService.get_file_from_bucket(filename, bucket)
