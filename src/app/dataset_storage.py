import json

from google.cloud import storage

storage_client = storage.Client()


def get_dataset(filename, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    dataset = json.loads(bucket.blob(filename).download_as_string())
    return dataset
