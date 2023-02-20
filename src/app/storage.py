import json
import os
from typing import Dict

from google.cloud import storage

storage_client = storage.Client()

if os.environ.get("KEYFILE_LOCATION"):
    storage_client = storage.Client().from_service_account_json(
        os.environ.get("KEYFILE_LOCATION")
    )
else:
    storage_client = storage.Client()

if os.environ.get("SCHEMA_BUCKET_NAME"):
    bucket = storage_client.bucket(os.environ.get("SCHEMA_BUCKET_NAME"))
else:
    raise Exception("You need to set SCHEMA_BUCKET_NAME")


def store_schema(schema: Dict, schema_id):
    filename = f"{schema['survey_id']}/{schema_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(schema, indent=2), content_type="application/json"
    )
    return filename


def get_schema(filename):
    schema = json.loads(bucket.blob(filename).download_as_string())
    return schema
