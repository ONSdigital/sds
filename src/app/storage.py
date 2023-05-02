import json

from config.config_factory import ConfigFactory
from google.cloud import storage

storage_client = storage.Client()
config = ConfigFactory.get_config()

try:
    bucket = storage_client.bucket(config.SCHEMA_BUCKET_NAME)
except Exception:
    if config.CONF == "docker-dev" or "IntegrationTestingDocker":
        bucket = storage_client.create_bucket("bucket")
    else:
        raise Exception("SCHEMA_BUCKET_NAME must be set")


def get_schema(filename):
    """Get the SDS schema from the schema bucket using the filename provided."""
    schema = json.loads(bucket.blob(filename).download_as_string())
    return schema
