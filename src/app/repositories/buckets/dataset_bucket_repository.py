import json

from google.cloud import storage
from logging_config import logging
from models.dataset_models import NewDatasetWithMetadata

logger = logging.getLogger(__name__)


class DatasetBucketRepository:
    def __init__(self):
        self.storage_client = storage.Client()

    def get_file_from_bucket(
        self, filename: str, bucket_name: str
    ) -> NewDatasetWithMetadata:
        """Used by the cloud function."""
        bucket = self.storage_client.bucket(bucket_name)

        try:
            return json.loads(bucket.blob(filename).download_as_string())

        except ValueError as e:
            logger.error(f"Invalid JSON in file {filename}: {e}")
            return None
