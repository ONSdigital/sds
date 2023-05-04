from models.dataset_models import NewDatasetWithMetadata


class DatasetValidatorService:
    @staticmethod
    def validate_filename(filename: str) -> None:
        if filename[-5:].lower() != ".json":
            raise RuntimeError(f"Invalid filetype received - {filename}")

    @staticmethod
    def validate_new_dataset(dataset: NewDatasetWithMetadata) -> None:
        DatasetValidatorService._validate_dataset_exists_in_bucket(dataset)
        DatasetValidatorService._validate_dataset_keys(dataset)

    @staticmethod
    def _validate_dataset_exists_in_bucket(dataset: NewDatasetWithMetadata):
        if dataset is None:
            raise RuntimeError("No corresponding dataset found in bucket")

    @staticmethod
    def _validate_dataset_keys(dataset: NewDatasetWithMetadata) -> None:
        isValid, message = DatasetValidatorService._check_for_missing_keys(dataset)

        if isValid is False:
            raise RuntimeError(f"Mandatory key(s) missing from JSON: {message}.")

        return dataset

    @staticmethod
    def _check_for_missing_keys(dataset: dict) -> tuple[bool, str]:
        """
        This method validates the JSON object to check if it contains all the mandatory keys.
        In the future, this can be enhanced further to validate nested JSON objects, for example, the 'data' element.
        """
        mandatory_keys = [
            "survey_id",
            "period_id",
            "sds_schema_version",
            "schema_version",
            "form_type",
            "data",
        ]

        missing_keys = DatasetValidatorService._collect_missing_keys_from_dataset(
            mandatory_keys, dataset
        )

        return (
            DatasetValidatorService._missing_keys_response(missing_keys)
            if len(missing_keys) > 0
            else DatasetValidatorService._valid_keys_response()
        )

    def _collect_missing_keys_from_dataset(mandatory_keys, dataset):
        return [
            mandatory_key
            for mandatory_key in mandatory_keys
            if mandatory_key not in dataset.keys()
        ]

    def _valid_keys_response() -> tuple[bool, str]:
        return True, ""

    def _missing_keys_response(missing_keys: list[str]) -> tuple[bool, str]:
        return False, ", ".join(missing_keys)
