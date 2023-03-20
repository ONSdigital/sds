import json
import os

from google.cloud import storage

storage_client = storage.Client()

# If the local development is used then, it will use those values to create the local storage.
if os.environ.get("DATASET_BUCKET_NAME"):
    bucket = storage_client.bucket(os.environ.get("DATASET_BUCKET_NAME"))
    if not bucket.exists():
        bucket = storage_client.create_bucket(os.environ.get("DATASET_BUCKET_NAME"))
else os.environ.get("STORAGE_EMULATOR_HOST"):
    bucket = storage_client.create_bucket("dataset_bucket")


def get_dataset(filename, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    dataset = json.loads(bucket.blob(filename).download_as_string())
    return dataset
