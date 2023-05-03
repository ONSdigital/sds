from models.dataset_models import NewDatasetWithMetadata


class DatasetValidatorService:
    @staticmethod
    def validate_filename(filename: str) -> None:
        if filename[-5:].lower() != ".json":
            raise RuntimeError(f"Invalid filetype received - {filename}")

    @staticmethod
    def validate_dataset_exists_in_bucket(dataset: NewDatasetWithMetadata):
        if dataset is None:
            raise RuntimeError("No corresponding dataset found in bucket")
