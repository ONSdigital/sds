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
        return dataset
    except ValueError as e:
        logger.error(f"Invalid JSON in the file {filename} - %s" % e)
        return None
