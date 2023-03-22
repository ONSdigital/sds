import json
import os
import uuid

import requests
from fastapi import FastAPI, Request
from google.cloud import storage

app = FastAPI()


@app.post("/")
async def dev_simulate_publish_dataset(request: Request):
    """
    Used to simulate SDX populating the bucket to manually fire the cloud event trigger
    """
    storage_client = storage.Client()
    bucket_name = os.environ.get("DATASET_BUCKET_NAME")
    storage_emulator_host = os.environ.get("STORAGE_EMULATOR_HOST")

    if bucket_name:
        bucket = storage_client.bucket(bucket_name)
        if not bucket.exists():
            bucket = storage_client.create_bucket(bucket_name)
    elif storage_emulator_host:
        bucket = storage_client.create_bucket("dataset_bucket")
    else:
        raise Exception("You need to set DATASET_BUCKET_NAME")

    # Create a guid as the filename before we publish it
    filename = f"{str(uuid.uuid4())}.json"

    # Save the dataset to the bucket
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(await request.json(), indent=2),
        content_type="application/json",
    )

    # Set the data object that will be sent to the cloud function
    event_data = {"bucket": "dataset_bucket", "name": filename}

    # request POST to new_dataset cloud function container (Simulates the trigger)
    url = "http://cloudfunction-new_dataset-sds:8080"

    headers = {
        "ce-specversion": "1.0",
        "ce-type": "google.cloud.audit.log.v1.written",
        "ce-source": "//SERVICE_NAME/projects/PROJECT_ID",
        "ce-id": "MESSAGE_ID",
        "ce-time": "ce-time",
        "Content-Type": "application/json; charset=utf-8",
    }

    requests.post(url, data=json.dumps(event_data), headers=headers)

    return {"filename": filename}
