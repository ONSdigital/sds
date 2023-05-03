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
        isValid = True
        mandatory_keys = [
            "survey_id",
            "period_id",
            "sds_schema_version",
            "schema_version",
            "form_type",
            "data",
        ]
        missing_keys = []
        message = ""

        for key in mandatory_keys:
            if key not in dataset.keys():
                missing_keys.append(key)

        if len(missing_keys) > 0:
            message = ", ".join(missing_keys)
            isValid = False

        return isValid, message
