import json

from google.cloud.storage.bucket import Bucket


class BucketOperationsService:
    @staticmethod
    def get_bucket_file_as_json(filename: str, bucket: Bucket) -> object:
        """Used by the cloud function."""
        return json.loads(bucket.blob(filename).download_as_string())
