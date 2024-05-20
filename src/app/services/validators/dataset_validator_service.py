from json import JSONDecodeError

from config.config_factory import config
from models.dataset_models import DatasetError, RawDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository

from ..dataset.dataset_writer_service import DatasetWriterService


class DatasetValidatorService:
    @staticmethod
    def validate_file_is_json(filename: str) -> None:
        """
        Validates the file extension is json.

        Parameters:
        filename (str): filename being validated.
        """

        DatasetValidatorService._validate_file_extension_is_json(filename)
        DatasetValidatorService._validate_file_content_is_json(filename)

    @staticmethod
    def _validate_file_extension_is_json(filename: str) -> None:
        """
        Raises a runtime error if the file type is not json.

        Parameters:
        filename (str): filename being validated.
        """

        if filename[-5:].lower() != ".json":
            pubsub_message = {
                "error": "Filetype error",
                "message": "Invalid filetype received.",
            }
            DatasetValidatorService.try_publish_dataset_error_to_topic(pubsub_message)
            raise RuntimeError(f"Invalid filetype received - {filename}")

    @staticmethod
    def _validate_file_content_is_json(filename: str) -> None:
        """
        Raises a runtime error if the file content is not json.

        Parameters:
        filename (str): filename being validated.
        """

        try:
            DatasetBucketRepository().get_dataset_file_as_json(filename)
        except JSONDecodeError:
            pubsub_message = {
                "error": "File content error",
                "message": "Invalid JSON content received.",
            }
            DatasetValidatorService.try_publish_dataset_error_to_topic(pubsub_message)
            raise RuntimeError("Invalid JSON content received.")

    @staticmethod
    def validate_raw_dataset(raw_dataset: RawDataset) -> None:
        """
        Validates the raw dataset.

        Parameters:
        raw_dataset (RawDataset): dataset being validated.
        """

        DatasetValidatorService._validate_dataset_exists_in_bucket(raw_dataset)
        DatasetValidatorService._validate_dataset_keys(raw_dataset)

    @staticmethod
    def _validate_dataset_exists_in_bucket(
        raw_dataset: RawDataset,
    ) -> None:
        """
        Validates the dataset returned from the bucket is not empty, raising a runtime error if not.

        Parameters:
        raw_dataset (RawDataset): dataset being validated.
        """
        if raw_dataset is None:
            raise RuntimeError("No corresponding dataset found in bucket")

    @staticmethod
    def _validate_dataset_keys(
        raw_dataset: RawDataset,
    ) -> None:
        """
        Validates the dataset has no mandatory keys missing from it, raising a runtime error if there are.

        Parameters:
        raw_dataset (RawDataset): dataset being validated.
        """

        isValid, message = DatasetValidatorService._check_for_missing_keys(raw_dataset)

        if isValid is False:
            pubsub_message = {
                "error": "Mandatory key(s) error",
                "message": "Mandatory key(s) missing from JSON.",
            }
            DatasetValidatorService.try_publish_dataset_error_to_topic(pubsub_message)
            raise RuntimeError(f"Mandatory key(s) missing from JSON: {message}.")

        return raw_dataset

    @staticmethod
    def _check_for_missing_keys(
        raw_dataset: RawDataset,
    ) -> tuple[bool, str]:
        """
        Returns a boolean and message depending on if there are keys missing from the data.

        Parameters:
        raw_dataset (RawDataset): dataset being validated.
        """
        mandatory_keys = [
            "survey_id",
            "period_id",
            "form_types",
            "schema_version",
            "data",
        ]

        missing_keys = DatasetValidatorService._collect_missing_keys_from_dataset(
            mandatory_keys, raw_dataset
        )

        return DatasetValidatorService._determine_missing_key_check_response(
            missing_keys
        )

    @staticmethod
    def _collect_missing_keys_from_dataset(
        mandatory_keys: list[str], raw_dataset: RawDataset
    ) -> list[str]:
        """
        Gets a list of any mandatory keys missing from the raw dataset.

        Parameters:
        mandatory_keys (list[str]): mandatory keys referenced.
        raw_dataset (RawDataset): dataset being validated.
        """

        return [
            mandatory_key
            for mandatory_key in mandatory_keys
            if mandatory_key not in raw_dataset.keys()
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

    @staticmethod
    def try_publish_dataset_error_to_topic(self, error_message: DatasetError) -> None:
        """
        Publishes dataset error response to google pubsub topic.

        Parameters:
        error_message: error message to be published.
        """
        dataset_repository = DatasetFirebaseRepository()
        dataset_writer_service = DatasetWriterService(dataset_repository)
        topic_id = config.PUBLISH_DATASET_ERROR_TOPIC_ID
        dataset_writer_service.try_publish_message_to_topic(error_message, topic_id)
