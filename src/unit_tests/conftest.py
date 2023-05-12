import json
import uuid
from datetime import datetime
from unittest.mock import MagicMock

import firebase_admin
import pytest
from config.config_factory import ConfigFactory
from fastapi.testclient import TestClient
from firebase_admin import firestore
from google.cloud import storage as google_cloud_storage
from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from services.shared.datetime_service import DatetimeService

from src.test_data import shared_test_data

config = ConfigFactory.get_config()


@pytest.fixture(autouse=True)
def datetime_mock():
    """
    Mocks datetime.now() wrapper to always return the same date and time in tests.
    """

    DatetimeService.get_current_date_and_time = MagicMock()
    DatetimeService.get_current_date_and_time.return_value = datetime(
        2023, 4, 20, 12, 0, 0
    )


@pytest.fixture(autouse=True)
def uuid_mock():
    """
    Mocks guid generation to always return the same guid.
    """

    uuid.uuid4 = MagicMock()
    uuid.uuid4.return_value = shared_test_data.test_guid


@pytest.fixture(autouse=True)
def cloud_bucket_credentials_mock(monkeypatch):
    """
    Mocks the google bucket credentials.
    """
    monkeypatch.setattr(google_cloud_storage, "Client", MagicMock())


@pytest.fixture(autouse=True)
def firebase_credentials_mock(monkeypatch):
    """
    Mocks firebase credentials.
    """
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())


@pytest.fixture()
def get_dataset_from_bucket_mock():
    """
    Mocks the application's google bucket boundaries.
    """
    with open(config.TEST_DATASET_PATH) as f:
        dataset_with_metadata: UnitDataset = json.load(f)

    DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
    DatasetBucketRepository.get_dataset_file_as_json.return_value = (
        dataset_with_metadata
    )


@pytest.fixture()
def new_dataset_mock():
    """
    Mocks the cloud function call.
    """
    from main import new_dataset

    yield new_dataset


@pytest.fixture
def test_client():
    """
    General client for hitting endpoints in tests, also mocking firebase credentials.
    """
    import app

    dataset_client = TestClient(app.app)
    yield dataset_client


@pytest.fixture
def test_client_no_server_exception():
    """
    This client is only used to test the 500 server error exception handler,
    therefore server exception for this client is suppressed
    """
    import app

    client = TestClient(app.app, raise_server_exceptions=False)
    yield client
