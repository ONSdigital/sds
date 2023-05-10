import json

from google.cloud import storage
from logging_config import logging
from models.dataset_models import NewDatasetWithMetadata

logger = logging.getLogger(__name__)


class BucketFileReader:
    def __init__(self):
        self.storage_client = storage.Client()

    def get_file_from_bucket(
        self, filename: str, bucket_name: str
    ) -> NewDatasetWithMetadata:
        """Used by the cloud function."""
        bucket = self.storage_client.bucket(bucket_name)

        try:
            dataset = json.loads(bucket.blob(filename).download_as_string())
            isValid, message = self.validate_keys(dataset)
            if isValid is True:
                return dataset
            else:
                logger.error(f"Mandatory key(s) missing from JSON: {message}")
                return None
        except ValueError as e:
            logger.error(f"Invalid JSON in file {filename}: {e}")
            return None

    def validate_keys(self, dataset: dict) -> tuple[bool, str]:
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
            "data",
        ]
        missing_keys = []
        message = ""

        for key in mandatory_keys:
            if key not in dataset.keys():
                missing_keys.append(key)

        if len(missing_keys) > 0:
            message = missing_keys.join(", ")
            isValid = False

        return isValid, message
