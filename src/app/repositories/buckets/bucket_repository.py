import json


class BucketRepository:
    def __init__(self, bucket_name: str):
        self.bucket = self.storage_client.bucket(bucket_name)

    def get_bucket_file_as_json(self, filename: str) -> object:
        """
        Gets a file from a google cloud bucket with a specific filename and loads it as json.

        Parameters:
        filename (str): name of file being loaded.
        """

        return json.loads(self.bucket.blob(filename).download_as_string())

    def empty_bucket(self) -> None:
        """
        Empties the bucket.
        """
        blobs = self.bucket.list_blobs()
        for blob in blobs:
            blob.delete()
