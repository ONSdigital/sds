from models.dataset_models import RawDatasetWithMetadata


class DatasetValidatorService:
    @staticmethod
    def validate_file_is_json(filename: str) -> None:
        """
        Raises a runtime error if the file type is not json.

        Parameters:
        filename (str): filename being validated.
        """

        if filename[-5:].lower() != ".json":
            raise RuntimeError(f"Invalid filetype received - {filename}")

    @staticmethod
    def validate_raw_dataset(raw_dataset_with_metadata: RawDatasetWithMetadata) -> None:
        """
        Validates the raw dataset.

        Parameters:
        raw_dataset_with_metadata (RawDatasetWithMetadata): dataset being validated.
        """

        DatasetValidatorService._validate_dataset_exists_in_bucket(
            raw_dataset_with_metadata
        )
        DatasetValidatorService._validate_dataset_keys(raw_dataset_with_metadata)

    @staticmethod
    def _validate_dataset_exists_in_bucket(
        raw_dataset_with_metadata: RawDatasetWithMetadata,
    ) -> None:
        """
        Validates the dataset returned from the bucket is not empty, raising a runtime error if not.

        Parameters:
        raw_dataset_with_metadata (RawDatasetWithMetadata): dataset being validated.
        """
        if raw_dataset_with_metadata is None:
            raise RuntimeError("No corresponding dataset found in bucket")

    @staticmethod
    def _validate_dataset_keys(
        raw_dataset_with_metadata: RawDatasetWithMetadata,
    ) -> None:
        """
        Validates the dataset has no mandatory keys missing from it, raising a runtime error if there are.

        Parameters:
        raw_dataset_with_metadata (RawDatasetWithMetadata): dataset being validated.
        """

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
        Returns a boolean and message depending on if there are keys missing from the data.

        Parameters:
        raw_dataset_with_metadata (RawDatasetWithMetadata): dataset being validated.
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
        """
        Gets a list of any mandatory keys missing from the raw dataset.

        Parameters:
        mandatory_keys (list[str]): mandatory keys referenced.
        raw_dataset_with_metadata (RawDatasetWithMetadata): dataset being validated.
        """

        return [
            mandatory_key
            for mandatory_key in mandatory_keys
            if mandatory_key not in dataset.keys()
        ]

    @staticmethod
    def _determine_missing_key_check_response(
        missing_keys: list[str],
    ) -> tuple[bool, str]:
        """
        Determines a response based on if there are any mandatory keys missing.

        Parameters:
        missing_keys (list[str]): list of missing keys.
        """

        return (
            DatasetValidatorService._missing_keys_response(missing_keys)
            if len(missing_keys) > 0
            else DatasetValidatorService._valid_keys_response()
        )

    @staticmethod
    def _valid_keys_response() -> tuple[bool, str]:
        """
        Response for when no keys are missing.
        """

        return True, ""

    @staticmethod
    def _missing_keys_response(missing_keys: list[str]) -> tuple[bool, str]:
        """
        Response for when there are missing keys.

        Parameters:
        missing_keys (list[str]): list of missing keys.
        """

        return False, ", ".join(missing_keys)
