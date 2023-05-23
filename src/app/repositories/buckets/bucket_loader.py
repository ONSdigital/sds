from config.config_factory import ConfigFactory
from google.cloud import exceptions, storage

config = ConfigFactory.get_config()

g_schema_bucket = None
g_dataset_bucket = None


class BucketLoader:
    def __init__(self):
        pass

    def get_or_create_bucket(self, bucket, bucket_name):
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

    def get_or_create_schema_bucket(self):
        global g_schema_bucket
        g_schema_bucket = self.get_or_create_bucket(
            g_schema_bucket, config.SCHEMA_BUCKET_NAME
        )
        return g_schema_bucket

    def get_or_create_dataset_bucket(self, bucket_name):
        global g_dataset_bucket
        g_dataset_bucket = self.get_or_create_bucket(g_dataset_bucket, bucket_name)
        return g_dataset_bucket
