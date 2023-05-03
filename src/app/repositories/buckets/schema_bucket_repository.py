import json

from config.config_factory import ConfigFactory
from google.cloud import storage
from models.schema_models import Schema
from services.shared.bucket_operations_service import BucketOperationsService


class SchemaBucketRepository:
    def __init__(self):
        self.storage_client = storage.Client()
        self.config = ConfigFactory.get_config()

        try:
            self.bucket = self.storage_client.bucket(self.config.SCHEMA_BUCKET_NAME)
        except Exception:
            if self.config.CONF == "docker-dev" or "IntegrationTestingDocker":
                self.bucket = self.storage_client.create_bucket("bucket")
            else:
                raise Exception("SCHEMA_BUCKET_NAME must be set")

    def store_schema_json(self, filename: str, schema: Schema) -> None:
        blob = self.bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(schema.dict(by_alias=True), indent=2),
            content_type="application/json",
        )

    def get_bucket_file_as_json(self, filename):
        """Get the SDS schema from the schema bucket using the filename provided."""
        return BucketOperationsService.get_file_from_bucket(filename, self.bucket) or None
