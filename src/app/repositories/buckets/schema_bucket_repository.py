import json

from exception import exceptions
from logging_config import logging
from repositories.buckets.bucket_loader import bucket_loader
from repositories.buckets.bucket_repository import BucketRepository

logger = logging.getLogger(__name__)


class SchemaBucketRepository(BucketRepository):
    def __init__(self):
        self.bucket = bucket_loader.get_schema_bucket()

    def store_schema_json(self, filename: str, schema: dict) -> None:
        """
        Stores schema in google bucket as json.

        Parameters:
        filename (str): filename of uploaded json schema.
        schema (Schema): schema being stored.
        """
        blob = self.bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(schema, indent=2),
            content_type="application/json",
        )

    def get_schema_file_as_json(self, filename: str) -> dict:
        """
        Get the SDS schema from the schema bucket using the filename provided.

        Parameters:
        filename (str): filename of the retreived json schema
        """
        try:
            return self.get_bucket_file_as_json(filename)
        except Exception as exc:
            logger.error("Schema not found")
            raise exceptions.ExceptionNoSchemaFound from exc
