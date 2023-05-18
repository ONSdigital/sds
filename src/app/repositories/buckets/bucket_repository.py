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

    def delete_bucket_file(self, filename: str) -> None:
        """
        Deletes a file with the specific filename from the bucket.

        Parameters:
        filename: name of the file being deleted.
        """
        self.bucket.blob(filename).delete()
