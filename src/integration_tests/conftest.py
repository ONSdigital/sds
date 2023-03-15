import json
import os
from time import sleep
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
    """
    When talking to the real API endpoint we wrap the requests library with functions calls
    that match the client test library. Because we are dealing with a real system that potentially
    has delays we make use of a retry strategy. This will retry up to 5 times with an exponential
    gap between retries.
    """

    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        self.headers = headers
        retry_strategy = Retry(
            total=5,  # Retry for up to 5 times
            backoff_factor=0.5,  # Wait between retries, increasing each time (0.5, 1.5, 3.5, 7.5, 15.5)
            status_forcelist=[404],  # Retry on these status codes
        )
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def get(self, endpoint):
        return self.session.get(f"{self.api_url}{endpoint}", headers=self.headers)

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
    real Cloud Function, so emulate the behaviour of the new_dataset function instead. If we are
    talking to the real Cloud Function but not the real API, we wait 3 seconds for the
    cloud function to complete it's processing. For testing the real API we have a better way of
    handling this delay using automated requests retries.
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
    elif not os.environ.get("API_URL"):
        sleep(3)


@pytest.fixture
def bucket_loader():
    return upload_dataset
