import json

from google.cloud.storage.bucket import Bucket


class BucketOperationsService:
    @staticmethod
    def get_bucket_file_as_json(filename: str, bucket: Bucket) -> object:
        """
        Gets a file from a google cloud bucket with a specific filename and loads it as json.

        Parameters:
        filename (str): name of file being loaded.
        bucket (Bucket): bucket being accessed.
        """

        return json.loads(bucket.blob(filename).download_as_string())
