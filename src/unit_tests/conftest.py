from unittest.mock import MagicMock

import firebase_admin
import pytest
from coverage.annotate import os
from fastapi.testclient import TestClient
from firebase_admin import firestore
from google.cloud import storage as google_cloud_storage


@pytest.fixture
def database(monkeypatch):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())
    import database

    yield database


@pytest.fixture
def storage(monkeypatch):
    monkeypatch.setattr(google_cloud_storage, "Client", MagicMock())
    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"
    import storage

    storage.storage.Client().bucket(
        "hello"
    ).blob().download_as_string.return_value = '{"hello":"json"}'
    yield storage


@pytest.fixture
def client(database, storage):
    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"
    import app

    client = TestClient(app.app)
    yield client


@pytest.fixture
def cloud_functions(database, storage):
    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"
    import main

    yield main
