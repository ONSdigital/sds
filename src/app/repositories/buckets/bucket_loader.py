from config.config_factory import ConfigFactory
from google.cloud import exceptions, storage

config = ConfigFactory.get_config()


class BucketLoader:
    def __init__(self):
        self.schema_bucket = None
        self.dataset_bucket = None

    def __get_or_create_bucket(self, bucket, bucket_name):
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

    def get_schema_bucket(self, bucket_name):
        self.schema_bucket = self.__get_or_create_bucket(
            self.schema_bucket, bucket_name
        )
        return self.schema_bucket

    def get_dataset_bucket(self, bucket_name):
        self.dataset_bucket = self.__get_or_create_bucket(
            self.dataset_bucket, bucket_name
        )
        return self.dataset_bucket
