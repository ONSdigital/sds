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
from config.config_factory import ConfigFactory

config = ConfigFactory.get_config()


def pytest_sessionstart():
    """Create the buckets before running the test."""
    if config.CONF == "docker-dev":
        check_and_create_bucket(config.DATASET_BUCKET_NAME)
        check_and_create_bucket(config.SCHEMA_BUCKET_NAME)


def check_and_create_bucket(bucket_name: str) -> None:
    """
    Method to check if a bucket of the provided name exists and create if it dosent exist

    Parameters:
        bucket_name: the name of the bucket to check and create

    Returns:
        None
    """
    try:
        if not gcp_storage.Bucket(storage_client, bucket_name).exists():
            storage_client.create_bucket(bucket_name)
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
    if (
        config.CONF == "IntegrationTestingCloud"
        or config.CONF == "cloud-integration-test"
    ):
        try:
            config.GOOGLE_APPLICATION_CREDENTIALS
            auth_req = google.auth.transport.requests.Request()
            auth_token = google.oauth2.id_token.fetch_id_token(auth_req, config.API_URL)
        except Exception:
            auth_token = os.environ.get("ACCESS_TOKEN")

        client = RequestWrapper(
            config.API_URL, headers={"Authorization": f"Bearer {auth_token}"}
        )
    else:
        from app import app

        client = TestClient(app)
    yield client


def upload_dataset(filename, dataset):
    """
    If STORAGE_EMULATOR_HOST is set, we assume we can't talk to the
    real Cloud Function, so emulate the behaviour of the new_dataset function instead. If we are
    talking to the real Cloud Function but not the real API, we wait 5 seconds for the
    cloud function to complete it's processing. For testing the real API we have a better way of
    handling this delay using automated requests retries.
    """
    bucket = storage_client.bucket(config.DATASET_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )

    if config.CONF == "docker-dev":
        from main import new_dataset

        cloud_event = MagicMock()
        cloud_event.data = {
            "bucket": config.DATASET_BUCKET_NAME,
            "name": filename,
        }
        new_dataset(cloud_event=cloud_event)
    elif config.CONF == "cloud-dev" or "localSDS-test":
        sleep(5)


@pytest.fixture
def bucket_loader():
    return upload_dataset
