import json
import os

from google.cloud import storage

storage_client = storage.Client()


bucket_name = os.environ.get("DATASET_BUCKET_NAME")

if bucket_name:
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
elif os.environ.get("STORAGE_EMULATOR_HOST"):
    bucket = storage_client.create_bucket("dataset_bucket")


def get_dataset(filename, bucket_name):
    """Used by the cloud function."""
    bucket = storage_client.bucket(bucket_name)
    dataset = json.loads(bucket.blob(filename).download_as_string())
    return dataset
