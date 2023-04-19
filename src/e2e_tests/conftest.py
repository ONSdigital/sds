import json
from unittest.mock import MagicMock
import firebase_admin
from firebase_admin import firestore
from coverage.annotate import os

import pytest
from bucket.bucket_file_reader import BucketFileReader
from google.cloud import storage
from repositories.dataset_repository import DatasetRepository


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
def dataset_repository_mock(monkeypatch):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())
    DatasetRepository = MagicMock()
    monkeypatch.setattr(
        DatasetRepository,
        "get_dataset_with_survey_id",
        lambda self, survey_id: [{
            "dataset_id": "test_dataset_id",
            "survey_id": "test_survey_id",
            "period_id": "test_period_id",
            "title": "test_title",
            "sds_schema_version": "test_schema_version",
            "sds_published_at": "2023-04-14T12:13:23Z",
            "total_reporting_units": 1,
            "schema_version": "test_schema_version",
            "sds_dataset_version": 1,
            "filename": "test_filename.json",
            "form_type": "test_form_type",
        }],
    )
    monkeypatch.setattr(
        DatasetRepository, "create_new_dataset", lambda self, dataset_id, dataset: None
    )
    monkeypatch.setattr(
        DatasetRepository,
        "get_dataset_unit_collection",
        lambda self, dataset_id: [
            {"test": "data"},
            {"hello": "world"},
        ],
    )
    monkeypatch.setattr(
        DatasetRepository,
        "append_unit_to_dataset_units_collection",
        lambda self, units_collection, unit_data: None,
    )

    yield DatasetRepository

@pytest.fixture()
def new_dataset(monkeypatch, bucket_file_reader_mock, dataset_repository_mock):
    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"
    monkeypatch.setattr(storage, "Client", MagicMock())
    from main import new_dataset
    yield new_dataset    
