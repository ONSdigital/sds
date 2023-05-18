import json

import exception.exceptions as exceptions
from config.config_factory import ConfigFactory
from google.cloud import storage
from logging_config import logging
from models.schema_models import Schema
from repositories.buckets.bucket_repository import BucketRepository

logger = logging.getLogger(__name__)


class SchemaBucketRepository(BucketRepository):
    def __init__(self):
        self.storage_client = storage.Client()
        self.config = ConfigFactory.get_config()

        if not self.storage_client.bucket(self.config.SCHEMA_BUCKET_NAME).exists():
            self.bucket = self.storage_client.create_bucket(
                self.config.SCHEMA_BUCKET_NAME
            )
        else:
            self.bucket = self.storage_client.bucket(self.config.SCHEMA_BUCKET_NAME)

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
