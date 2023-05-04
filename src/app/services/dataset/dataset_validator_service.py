from models.dataset_models import RawDatasetWithMetadata


class DatasetValidatorService:
    @staticmethod
    def validate_filename(filename: str) -> None:
        if filename[-5:].lower() != ".json":
            raise RuntimeError(f"Invalid filetype received - {filename}")

    @staticmethod
    def validate_new_dataset(raw_dataset_with_metadata: RawDatasetWithMetadata) -> None:
        DatasetValidatorService._validate_dataset_exists_in_bucket(
            raw_dataset_with_metadata
        )
        DatasetValidatorService._validate_dataset_keys(raw_dataset_with_metadata)

    @staticmethod
    def _validate_dataset_exists_in_bucket(
        raw_dataset_with_metadata: RawDatasetWithMetadata,
    ) -> None:
        if raw_dataset_with_metadata is None:
            raise RuntimeError("No corresponding dataset found in bucket")

    @staticmethod
    def _validate_dataset_keys(
        raw_dataset_with_metadata: RawDatasetWithMetadata,
    ) -> None:
        isValid, message = DatasetValidatorService._check_for_missing_keys(
            raw_dataset_with_metadata
        )

        if isValid is False:
            raise RuntimeError(f"Mandatory key(s) missing from JSON: {message}.")

        return raw_dataset_with_metadata

    @staticmethod
    def _check_for_missing_keys(
        raw_dataset_with_metadata: RawDatasetWithMetadata,
    ) -> tuple[bool, str]:
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
            mandatory_keys, raw_dataset_with_metadata
        )

        return DatasetValidatorService._determine_missing_key_check_response(
            missing_keys
        )

    @staticmethod
    def _collect_missing_keys_from_dataset(
        mandatory_keys: list[str], dataset: RawDatasetWithMetadata
    ) -> list[str]:
        return [
            mandatory_key
            for mandatory_key in mandatory_keys
            if mandatory_key not in dataset.keys()
        ]

    @staticmethod
    def _determine_missing_key_check_response(
        missing_keys: list[str],
    ) -> tuple[bool, str]:
        return (
            DatasetValidatorService._missing_keys_response(missing_keys)
            if len(missing_keys) > 0
            else DatasetValidatorService._valid_keys_response()
        )

    @staticmethod
    def _valid_keys_response() -> tuple[bool, str]:
        return True, ""

    @staticmethod
    def _missing_keys_response(missing_keys: list[str]) -> tuple[bool, str]:
        return False, ", ".join(missing_keys)
