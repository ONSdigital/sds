import json
import os
from unittest.mock import MagicMock

import google.auth.transport.requests
import google.oauth2.id_token
import pytest
import requests
from fastapi.testclient import TestClient
from google.cloud import storage as gcp_storage

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
    if api_url:
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            auth_req = google.auth.transport.requests.Request()
            auth_token = google.oauth2.id_token.fetch_id_token(auth_req, api_url)
        else:
            # credentials, project_id = google.auth.default(
            #     scopes=["https://www.googleapis.com/auth/cloud-platform"]
            # )
            # if credentials.expired and credentials.refresh_token:
            #     credentials.refresh(google.auth.transport.requests.Request())
            # auth_token = credentials.token
            auth_token = os.environ.get("ACCESS_TOKEN")
            print(f"auth_token: {auth_token}")

        client = RequestWrapper(
            api_url, headers={"Authorization": f"Bearer {auth_token}"}
        )
    else:
        from app import app

        client = TestClient(app)
    yield client


def upload_dataset(filename, dataset):
    """If STORAGE_EMULATOR_HOST is set, we assume we can't talk to the real thing so emulate
    the behaviour of the new_dataset function instead."""
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
