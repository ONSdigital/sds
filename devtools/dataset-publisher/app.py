import json
import uuid

import requests
from config_factory import ConfigFactory
from fastapi import FastAPI, Request
from google.cloud import storage

app = FastAPI()

config = ConfigFactory.get_config()


@app.post("/")
async def dev_simulate_publish_dataset(request: Request, filename: str | None = None):
    """
    Used to simulate SDX populating the bucket to manually fire the cloud event trigger
    """
    storage_client = storage.Client()

    # Check if the dataset bucket exists.
    dataset_bucket = setup_local_storage(config.DATASET_BUCKET_NAME, storage_client)

    # If filename is not provided, create a guid as the filename before we publish it
    if filename in (None, ""):
        filename = f"{uuid.uuid4()!s}.json"

    # Save the dataset to the bucket
    blob = dataset_bucket.blob(filename)
    data = await request.body()
    blob.upload_from_string(
        data.decode("utf-8"),
        content_type="text/plain",
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

    requests.post(url, data=json.dumps(event_data), headers=headers, timeout=30)

    return {"filename": filename}


def setup_local_storage(bucket_name, storage_client):
    """
    This is to setup the dataset bucket in the local storage emulator.
    This is to check if the buckets exists and if it doe not, then it will create it. This is due to the fact that the
    storage emulator requires a 'bucket' to be created on start. If bucket exist, all files are deleted to ensure
    """
    if bucket_name:
        bucket = storage_client.bucket(bucket_name)
        if bucket.exists():
            blobs = bucket.list_blobs()
            for blob in blobs:
                blob.delete()

            return bucket
        
        return storage_client.create_bucket(bucket_name)
    else:
        raise Exception("You need to set a name for the bucket")
