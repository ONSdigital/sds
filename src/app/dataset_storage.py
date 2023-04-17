import json

from google.cloud import storage
from logging_config import logging


logger = logging.getLogger(__name__)
storage_client = storage.Client()


def get_dataset(filename, bucket_name):
    """Used by the cloud function."""
    bucket = storage_client.bucket(bucket_name)
    try:
        dataset = json.loads(bucket.blob(filename).download_as_string())
        return dataset        
    except ValueError as e:
        logger.error("Invalid JSON file contents - %s" % e)
        return None
