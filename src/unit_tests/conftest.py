import json
import uuid
from datetime import datetime
from typing import Generator
from unittest.mock import MagicMock

import firebase_admin
import pytest
from bucket.bucket_file_reader import BucketFileReader
from config.config_factory import ConfigFactory
from coverage.annotate import os
from fastapi.testclient import TestClient
from firebase_admin import firestore
from google.cloud import storage as google_cloud_storage
from google.cloud.firestore_v1.document import DocumentSnapshot
from repositories.dataset_repository import DatasetRepository
from services.datetime_service import DatetimeService

from src.test_data.new_dataset import dataset_test_data

config = ConfigFactory.get_config()


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
def cloud_function(database, storage):
    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"
    import main

    yield main


@pytest.fixture()
def datetime_mock():
    DatetimeService.get_current_date_and_time = MagicMock()
    DatetimeService.get_current_date_and_time.return_value = datetime(
        2023, 4, 20, 12, 0, 0
    )


@pytest.fixture()
def uuid_mock():
    uuid.uuid4 = MagicMock()
    uuid.uuid4.return_value = dataset_test_data.test_dataset_id


def mock_document_snapshot_generator() -> Generator[DocumentSnapshot, None, None]:
    dataset_with_survey_id_data = MagicMock(spec=DocumentSnapshot)
    dataset_with_survey_id_data.to_dict.return_value = (
        dataset_test_data.dataset_metadata_dto
    )

    yield dataset_with_survey_id_data


@pytest.fixture()
def repository_boundaries_mock():
    DatasetRepository.get_dataset_with_survey_id = MagicMock()
    DatasetRepository.get_dataset_with_survey_id.return_value = (
        mock_document_snapshot_generator()
    )

    DatasetRepository.create_new_dataset = MagicMock()
    DatasetRepository.create_new_dataset.return_value = None

    DatasetRepository.get_dataset_unit_collection = MagicMock()
    DatasetRepository.get_dataset_unit_collection.return_value = (
        dataset_test_data.existing_dataset_unit_data_collection
    )

    DatasetRepository.append_unit_to_dataset_units_collection = MagicMock()
    DatasetRepository.append_unit_to_dataset_units_collection.return_value = None


@pytest.fixture()
def cloud_bucket_mock(monkeypatch):
    monkeypatch.setattr(google_cloud_storage, "Client", MagicMock())

    with open(config.TEST_DATASET_PATH) as f:
        dataset_with_metadata = json.load(f)

    BucketFileReader.get_file_from_bucket = MagicMock()
    BucketFileReader.get_file_from_bucket.return_value = dataset_with_metadata


@pytest.fixture()
def new_dataset_mock(monkeypatch, cloud_bucket_mock):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())

    os.environ["SCHEMA_BUCKET_NAME"] = "the bucket name"

    from main import new_dataset

    yield new_dataset
