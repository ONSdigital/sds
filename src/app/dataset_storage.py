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
        isValid, message = validate_keys(dataset)
        if isValid is True:
            return dataset
        else:
            logger.error(f"The mandatory key(s) {message} is/are missing in the JSON object.")
            return None
    except ValueError as e:
        logger.error(f"Invalid JSON in the file {filename} - %s" % e)
        return None


def validate_keys(dataset: dict) -> tuple[bool, str]:
    """
    This method validates the JSON object to check if it contains all the mandatory keys.
    """
    isValid = True
    mandatory_keys = ['survey_id', 'period_id', 'sds_schema_version', 'schema_version', 'form_type', 'data']
    missing_keys = []
    message = ""

    for key in mandatory_keys:
        if key not in dataset.keys():
            missing_keys.append(key)
    
    if len(missing_keys) > 0:
        message = ', '.join(missing_keys)
        isValid = False

    return isValid, message
