from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.validators.dataset_validator_service import DatasetValidatorService


class DatasetBucketService:
    def __init__(self, bucket_name):
        self.dataset_bucket_repository = DatasetBucketRepository(bucket_name)

    def get_dataset_with_cleanup(self, filename: str) -> UnitDataset:
        DatasetValidatorService.validate_file_is_json(filename)

        raw_dataset_with_metadata = (
            self.dataset_bucket_repository.get_dataset_file_as_json(filename)
        )
        self.dataset_bucket_repository.empty_bucket()

        DatasetValidatorService.validate_raw_dataset(raw_dataset_with_metadata)

        return raw_dataset_with_metadata
