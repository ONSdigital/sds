import json
import os
import uuid

from google.cloud import storage

storage_client = storage.Client()

DATASET_BUCKET = os.environ.get("DATASET_BUCKET")
bucket = storage_client.bucket(DATASET_BUCKET)


def test_dataset():
    with open("../test_data/dataset.json") as f:
        dataset = json.load(f)
    dataset_id = str(uuid.uuid4())
    filename = f"{dataset_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )
