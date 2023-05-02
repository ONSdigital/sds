import json

from config.config_factory import ConfigFactory
from google.cloud import storage
from models.schema_models import Schema

config = ConfigFactory.get_config()


class SchemaBucketRepository:
    def __init__(self):
        self.storage_client = storage.Client()

        try:
            self.bucket = self.storage_client.bucket(config.SCHEMA_BUCKET_NAME)
        except Exception:
            if config.CONF == "docker-dev" or "IntegrationTestingDocker":
                self.bucket = self.storage_client.create_bucket("bucket")
            else:
                raise Exception("SCHEMA_BUCKET_NAME must be set")

    def store_schema_json(self, filename: str, schema: Schema) -> None:
        blob = self.bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(schema.dict(by_alias=True), indent=2),
            content_type="application/json",
        )
