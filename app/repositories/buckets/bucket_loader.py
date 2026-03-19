from google.cloud import exceptions, storage

import app.exception.exceptions as exception
from app.config.config_factory import config
from app.logging_config import logging

logger = logging.getLogger(__name__)

class BucketLoader:
    schema_bucket: storage.Bucket | None = None
    __storage_client: storage.Client

    def __init__(self, storage_client: storage.Client) -> None:
        self.__storage_client = storage_client

        if config.CONF == "unit":
            return

        self.schema_bucket = self._initialise_bucket(config.SCHEMA_BUCKET_NAME)

    def get_schema_bucket(self) -> storage.Bucket:
        """
        Get the schema bucket from Google cloud
        """
        return self.schema_bucket

    def _initialise_bucket(self, bucket_name) -> storage.Bucket:
        """
        Connect to google cloud storage client using PROJECT_ID
        For local environment, if bucket does not exist, then create the bucket
        Else connect to the bucket

        Parameters:
        bucket_name (str): The bucket name

        Returns:
        storage.Bucket: The bucket object
        """
        try:
            bucket = self.__storage_client.get_bucket(
                bucket_name,
            )
        except exceptions.NotFound as exc:
            logger.debug("Error getting bucket")

            if config.CONF != "docker-dev":
                raise exception.ExceptionBucketNotFound from exc

            # For local environment, if bucket does not exist, create it
            bucket = self.__storage_client.create_bucket(bucket_name)

        return bucket


client = storage.Client(project=config.PROJECT_ID)
bucket_loader = BucketLoader(client)
