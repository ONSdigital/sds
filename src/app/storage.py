from dataclasses import asdict

from google.cloud import storage
import json
import os

from models import Schema

storage_client = storage.Client()

if os.environ.get("KEYFILE_LOCATION"):
    storage_client = storage.Client().from_service_account_json(os.environ.get("KEYFILE_LOCATION"))
else:
    storage_client = storage.Client()

if os.environ.get("SCHEMA_BUCKET_NAME"):
    bucket = storage_client.bucket(os.environ.get("SCHEMA_BUCKET_NAME"))
else:
    raise Exception("You need to set SCHEMA_BUCKET_NAME")


def store_schema(schema: Schema, schema_id):
    filename = f"{schema.survey_id}/{schema_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(asdict(schema), indent=2), content_type='application/json')
    return filename
