from config.config_factory import ConfigFactory
from logging_config import logging
from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.validators.dataset_validator_service import DatasetValidatorService

logger = logging.getLogger(__name__)


class DatasetBucketService:
    def __init__(self, bucket_name):
        self.config = ConfigFactory.get_config()

        self.bucket_name = bucket_name
        self.dataset_bucket_repository = DatasetBucketRepository(bucket_name)

    def get_dataset_with_cleanup(self, filename: str) -> UnitDataset:
        DatasetValidatorService.validate_file_is_json(filename)

        raw_dataset_with_metadata = (
            self.dataset_bucket_repository.get_dataset_file_as_json(filename)
        )

        if self.config.AUTODELETE_DATASET_BUCKET_FILE:
            self._try_empty_bucket()

        DatasetValidatorService.validate_raw_dataset(raw_dataset_with_metadata)

        return raw_dataset_with_metadata

    def _try_empty_bucket(self) -> None:
        try:
            self.dataset_bucket_repository.empty_bucket()
        except Exception as e:
            logger.debug(f"Failed to empty bucket {self.bucket_name} with error: {e}")
            raise RuntimeError("Failed to empty dataset bucket.")
