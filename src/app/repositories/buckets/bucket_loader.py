from config.config_factory import ConfigFactory
from google.cloud import exceptions, storage

config = ConfigFactory.get_config()


class BucketLoader:
    def __init__(self):
        self.schema_bucket = None
        self.dataset_bucket = None
        self._set_buckets()

    def get_schema_bucket(self) -> storage.Bucket:
        """
        Get the schema bucket from Google cloud
        """
        return self.schema_bucket

    def get_dataset_bucket(self) -> storage.Bucket:
        """
        Get the dataset bucket from Google cloud
        """
        return self.dataset_bucket

    def _get_or_create_bucket(self, bucket, bucket_name) -> storage.Bucket:
        """
        Connect to google cloud storage client using PROJECT_ID
        If bucket does not exists, then create the bucket
        Else connect to the bucket

        Parameters:
        bucket (storage.Bucket): The bucket that is currently handling
        bucket_name (str): The bucket name
        """
        if config.CONF == "unit":
            return None

        if not bucket:
            __storage_client = storage.Client(project=config.PROJECT_ID)
            try:
                bucket = __storage_client.get_bucket(
                    bucket_name,
                )
            except exceptions.NotFound:
                bucket = __storage_client.create_bucket(
                    bucket_name,
                )

        return bucket

    def _set_buckets(self):
        """
        Setup the schema and dataset buckets
        """
        self.schema_bucket = self._get_or_create_bucket(
            self.schema_bucket, config.SCHEMA_BUCKET_NAME
        )

        self.dataset_bucket = self._get_or_create_bucket(
            self.dataset_bucket, config.DATASET_BUCKET_NAME
        )
