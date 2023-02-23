import json
import os

from google.cloud import storage
from models import Schema

storage_client = storage.Client()

if os.environ.get("SCHEMA_BUCKET_NAME"):
    bucket = storage_client.bucket(os.environ.get("SCHEMA_BUCKET_NAME"))
elif os.environ.get("STORAGE_EMULATOR_HOST"):
    bucket = storage_client.create_bucket("bucket")
else:
    raise Exception("You need to set SCHEMA_BUCKET_NAME")


def store_schema(schema: Schema, schema_id):
    filename = f"{schema.survey_id}/{schema_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(schema.dict(by_alias=True), indent=2),
        content_type="application/json",
    )
    return filename


def get_schema(filename):
    schema = json.loads(bucket.blob(filename).download_as_string())
    return schema


def get_dataset(filename, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    dataset = json.loads(bucket.blob(filename).download_as_string())
    return dataset
