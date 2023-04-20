import json
from unittest.mock import MagicMock

import firebase_admin
import pytest
from bucket.bucket_file_reader import BucketFileReader
from coverage.annotate import os
from firebase_admin import firestore
from google.cloud import storage


@pytest.fixture()
def bucket_file_reader_mock(monkeypatch):
    with open("../test_data/dataset.json") as f:
        dataset_with_metadata = json.load(f)

    monkeypatch.setattr(storage, "Client", MagicMock())
    monkeypatch.setattr(
        BucketFileReader,
        "get_file_from_bucket",
        lambda self, filename, bucket_name: dataset_with_metadata,
    )


@pytest.fixture()
def new_dataset(monkeypatch, bucket_file_reader_mock):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())

    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"
    monkeypatch.setattr(storage, "Client", MagicMock())
    from main import new_dataset

    yield new_dataset
