import json

from google.cloud import storage
from logging_config import logging

logger = logging.getLogger(__name__)
storage_client = storage.Client()


def get_dataset(filename, bucket_name):
    """
    Used by the cloud function.
    * Process if the file content is proper JSON syntax or else log error.
    """
    bucket = storage_client.bucket(bucket_name)
    try:
        dataset = json.loads(bucket.blob(filename).download_as_string())
        isValid, missing_keys = validate_keys_dataset(dataset)
        if isValid is True:
            return dataset
        else:
            message = ""
            for key in missing_keys:
                message = message + key + ", "
            logger.error(f"The keys {message} are missing in the JSON object")        
            return None
    except ValueError as e:
        logger.error(f"Invalid JSON in the file {filename} - %s" % e)
        return None


def validate_keys_dataset(dataset):
    isValid = True
    missing_keys = []

    if "survey_id" not in dataset.keys():
        missing_keys.append("survey_id")
    if "period_id" not in dataset.keys():
        missing_keys.append("period_id")
    if "sds_schema_version" not in dataset.keys():
        missing_keys.append("sds_schema_ version")
    if "schema_version" not in dataset.keys():
        missing_keys.append("schema_version")
    if "form_type" not in dataset.keys():
        missing_keys.append("schema_version")

    if len(missing_keys) > 0:
        isValid = False

    return isValid, missing_keys
