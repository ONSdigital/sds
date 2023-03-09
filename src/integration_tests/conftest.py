import os
from unittest.mock import MagicMock

import pytest
import requests
from fastapi.testclient import TestClient
from google.cloud import storage as gcp_storage
import json
from main import new_dataset


storage_client = gcp_storage.Client()


class RequestWrapper:
    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        self.headers = headers

    def get(self, endpoint):
        return requests.get(f"{self.api_url}{endpoint}", headers=self.headers)

    def post(self, endpoint, json):
        return requests.post(
            f"{self.api_url}{endpoint}", headers=self.headers, json=json
        )


@pytest.fixture
def client():
    api_url = os.environ.get("API_URL")
    auth_token = os.environ.get("AUTH_TOKEN")
    if api_url:
        if auth_token:
            client = RequestWrapper(
                api_url, headers={"Authorization": f"Bearer {auth_token}"}
            )
        else:
            client = RequestWrapper(api_url)
    else:
        from app import app

        client = TestClient(app)
    yield client


def upload_dataset(filename, dataset):
    """If GOOGLE_APPLICATION_CREDENTIALS is set, we
    assume we can talk to the real thing and make use
    of the hosted cloud function."""
    dataset_bucket = os.environ.get("DATASET_BUCKET")
    bucket = storage_client.bucket(dataset_bucket)
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        cloud_event = MagicMock()
        cloud_event.data = {
            "bucket": dataset_bucket,
            "name": filename,
        }
        new_dataset(cloud_event=cloud_event)


@pytest.fixture
def bucket_loader():
    return upload_dataset
