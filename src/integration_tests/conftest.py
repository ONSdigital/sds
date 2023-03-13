import json
import os
from unittest.mock import MagicMock

import google.auth.transport.requests
import google.oauth2.id_token
import pytest
import requests
from fastapi.testclient import TestClient
from google.cloud import exceptions
from google.cloud import storage as gcp_storage
from requests.adapters import HTTPAdapter
from urllib3 import Retry

storage_client = gcp_storage.Client()


def pytest_sessionstart():
    """Create the buckets before running the test."""
    if os.environ.get("STORAGE_EMULATOR_HOST"):
        try:
            storage_client.create_bucket(os.environ.get("DATASET_BUCKET"))
        except exceptions.Conflict:
            pass
        try:
            storage_client.create_bucket(os.environ.get("SCHEMA_BUCKET_NAME"))
        except exceptions.Conflict:
            pass





class RequestWrapper:
    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        self.headers = headers
        retry_strategy = Retry(
            total=50,  # Retry for up to 50 times
            backoff_factor=0.1,  # Wait between retries, increasing each time (0.1s, 0.2s, 0.4s, ...)
            status_forcelist=[404],  # Retry on these status codes
        )
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def get(self, endpoint):
        return self.get(f"{self.api_url}{endpoint}", headers=self.headers)

    def post(self, endpoint, json):
        return requests.post(
            f"{self.api_url}{endpoint}", headers=self.headers, json=json
        )


@pytest.fixture
def client():
    api_url = os.environ.get("API_URL")
    if api_url:
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            auth_req = google.auth.transport.requests.Request()
            auth_token = google.oauth2.id_token.fetch_id_token(auth_req, api_url)
        else:
            auth_token = os.environ.get("ACCESS_TOKEN")

        client = RequestWrapper(
            api_url, headers={"Authorization": f"Bearer {auth_token}"}
        )
    else:
        from app import app

        client = TestClient(app)
    yield client


def upload_dataset(filename, dataset):
    """
    If STORAGE_EMULATOR_HOST is set, we assume we can't talk to the
    real Cloud Function, so emulate the behaviour of the new_dataset function instead.
    """
    dataset_bucket = os.environ.get("DATASET_BUCKET")
    bucket = storage_client.bucket(dataset_bucket)
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )
    if os.environ.get("STORAGE_EMULATOR_HOST"):
        from main import new_dataset

        cloud_event = MagicMock()
        cloud_event.data = {
            "bucket": dataset_bucket,
            "name": filename,
        }
        new_dataset(cloud_event=cloud_event)


@pytest.fixture
def bucket_loader():
    return upload_dataset
