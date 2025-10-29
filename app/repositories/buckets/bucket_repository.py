import json


class BucketRepository:
    def get_bucket_file_as_json(self, filename: str) -> object:
        """
        Gets a file from a google cloud bucket with a specific filename and loads it as json.

        Parameters:
        filename (str): name of file being loaded.

        Returns: object: the file loaded as json.
        """
        return json.loads(self.bucket.blob(filename).download_as_string())
