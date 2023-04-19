import json

from google.cloud import storage


class BucketFileReader:
    def __init__(self):
        self.storage_client = storage.Client()

    def get_file_from_bucket(self, filename: str, bucket_name: str):
        """Used by the cloud function."""
        bucket = self.storage_client.bucket(bucket_name)
        return json.loads(bucket.blob(filename).download_as_string())
