from config.config_factory import ConfigFactory
from logging_config import logging
from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.validators.dataset_validator_service import DatasetValidatorService

logger = logging.getLogger(__name__)


class DatasetBucketService:
    def __init__(self, bucket_name):
        self.config = ConfigFactory.get_config()
        self.dataset_bucket_repository = DatasetBucketRepository(bucket_name)
        self.bucket_name = bucket_name

    def get_and_validate_dataset(self, filename: str) -> UnitDataset:
        """
        Validates and retrieves dataset from bucket

        Parameters:
        filename: name of file being retrieved from bucket
        """
        DatasetValidatorService.validate_file_is_json(filename)

        raw_dataset_with_metadata = (
            self.dataset_bucket_repository.get_dataset_file_as_json(filename)
        )

        DatasetValidatorService.validate_raw_dataset(raw_dataset_with_metadata)

        if self.config.AUTODELETE_DATASET_BUCKET_FILE is True:
            self._try_delete_bucket_file(filename)

        return raw_dataset_with_metadata

    def _try_delete_bucket_file(self, filename) -> None:
        """
        Tries to delete a file from the bucket, raises an error on failure.
        """
        try:
            self.dataset_bucket_repository.delete_bucket_file(filename)
        except Exception as e:
            logger.debug(
                f"Failed to delete file {filename} from bucket {self.bucket_name} with error: {e}"
            )
            raise RuntimeError("Failed to delete file from dataset bucket.")
