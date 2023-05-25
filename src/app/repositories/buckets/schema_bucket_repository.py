import json

import exception.exceptions as exceptions
from config.config_factory import ConfigFactory
from logging_config import logging
from models.schema_models import Schema
from repositories.buckets.bucket_loader import BucketLoader
from repositories.buckets.bucket_repository import BucketRepository

logger = logging.getLogger(__name__)

config = ConfigFactory.get_config()
bucket_loader = BucketLoader()


class SchemaBucketRepository(BucketRepository):
    def __init__(self):
        self.bucket = bucket_loader.get_schema_bucket()

    def store_schema_json(self, filename: str, schema: Schema) -> None:
        """
        Stores schema in google bucket as json.

        Parameters:
        filename (str): filename of uploaded json schema.
        schema (Schema): schema being stored.
        """
        blob = self.bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(schema.dict(by_alias=True), indent=2),
            content_type="application/json",
        )

    def get_schema_file_as_json(self, filename: str) -> Schema:
        """Get the SDS schema from the schema bucket using the filename provided."""
        try:
            return self.get_bucket_file_as_json(filename)
        except Exception:
            logger.error("Schema not found")
            raise exceptions.ExceptionNoSchemaFound
