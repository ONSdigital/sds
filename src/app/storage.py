import json

from config.config_factory import ConfigFactory
from google.cloud import storage
from models import Schema

storage_client = storage.Client()
config = ConfigFactory.get_config()

try:
    bucket = storage_client.bucket(config.SCHEMA_BUCKET_NAME)
except Exception:
    if config.CONF == "docker-dev" or "IntegrationTestingDocker":
        bucket = storage_client.create_bucket("bucket")
    else:
        raise Exception("SCHEMA_BUCKET_NAME must be set")


def store_schema(schema: Schema, schema_id):
    """Store the schema JSON file in the bucket using the schema_id as the filename."""
    filename = f"{schema.survey_id}/{schema_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(schema.dict(by_alias=True), indent=2),
        content_type="application/json",
    )
    return filename


def get_schema(filename):
    """Get the SDS schema from the schema bucket using the filename provided."""
    schema = json.loads(bucket.blob(filename).download_as_string())
    return schema
