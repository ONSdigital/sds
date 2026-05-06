import uuid
from datetime import datetime
from unittest.mock import MagicMock, Mock

import pytest
from fastapi.testclient import TestClient
from google.cloud import firestore

from app.dependencies import get_publisher_service
from app.services.shared.datetime_service import DatetimeService
from app.services.shared.publisher_service import PublisherService
from tests.test_data import shared_test_data


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
def firestore_credentials_mock(monkeypatch):
    """
    Mocks firestore credentials
    """
    mock_client = MagicMock()
    mock_client.transaction = MagicMock(return_value=MagicMock())
    mock_client.collection = MagicMock(return_value=MagicMock())

    monkeypatch.setattr(firestore, "Client", mock_client)


@pytest.fixture(autouse=True)
def pubsub_mock(test_client):
    """
    Mocks the google pubsub credentials.
    """
    app = test_client.app
    mock_pubsub = Mock(spec=PublisherService)
    app.dependency_overrides[get_publisher_service] = lambda: mock_pubsub

    yield mock_pubsub


@pytest.fixture
def test_client():
    """
    General client for hitting endpoints in tests, also mocking firebase credentials.
    """
    from app.main import app

    client = TestClient(app)
    yield client


@pytest.fixture
def test_client_no_server_exception():
    """
    This client is only used to test the 500 server error exception handler,
    therefore server exception for this client is suppressed
    """
    from app.main import app

    client = TestClient(app, raise_server_exceptions=False)
    yield client
