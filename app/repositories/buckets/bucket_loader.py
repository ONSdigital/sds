from google.cloud import exceptions, storage

from app.config import settings
from app.exception.exceptions import ExceptionBucketNotFound
from app.logging_config import logging

logger = logging.getLogger(__name__)


class BucketLoader:
    schema_bucket: storage.Bucket | None = None
    __storage_client = storage.Client

    def __init__(self, storage_client: storage.Client) -> None:
        self.__storage_client = storage_client

        if settings.CONF == "unit":
            return

        self.schema_bucket = self._initialise_bucket(settings.SCHEMA_BUCKET_NAME)

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
        """
        try:
            bucket = self.__storage_client.get_bucket(
                bucket_name,
            )
        except exceptions.NotFound as exc:
            logger.debug("Error getting bucket")

            if settings.CONF != "docker-dev":
                raise ExceptionBucketNotFound from exc

            # For local environment, if bucket does not exist, create it
            bucket = self.__storage_client.create_bucket(bucket_name)

        return bucket

client = storage.Client(project=settings.PROJECT_ID)
bucket_loader = BucketLoader(client)
