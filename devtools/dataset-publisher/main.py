import json
import logging
import os
import uuid

import functions_framework
from google.cloud import storage

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@functions_framework.cloud_event
def dev_publish_dataset(cloud_event):
    """
    Used to simulate SDX populating the bucket to manually fire the cloud event trigger
    """
    storage_client = storage.Client()

    if os.environ.get("DATASET_BUCKET_NAME"):
        bucket = storage_client.bucket(os.environ.get("DATASET_BUCKET_NAME"))
        if not bucket.exists():
            bucket = storage_client.create_bucket(os.environ.get("DATASET_BUCKET_NAME"))
    elif os.environ.get("STORAGE_EMULATOR_HOST"):
        bucket = storage_client.create_bucket("dataset_bucket")
    else:
        raise Exception("You need to set DATASET_BUCKET_NAME")

    filename = f"{str(uuid.uuid4())}.json"

    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(cloud_event.data, indent=2),
        content_type="application/json",
    )
    logging.info(f"Filename used : {filename}")
    return filename
