import uuid
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests
from fastapi.testclient import TestClient
from google.cloud.firestore import Transaction
from mockfirestore import MockFirestore

from app.dependencies import get_publisher_service, get_firebase_loader
from app.services.dataset_service import DatasetService
from app.services.schema_service import SchemaService
from app.util.firebase_loader import FirebaseLoader
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
def firestore_mock(test_client):
    app = test_client.app
    mock_firestore = Mock(spec=FirebaseLoader)
    mock_firestore.client = MockFirestore()
    mock_firestore.get_client.return_value = mock_firestore.client
    app.dependency_overrides[get_firebase_loader] = lambda: mock_firestore

    yield mock_firestore

    mock_firestore.client.reset()


@pytest.fixture(autouse=True)
def transaction_mock(firestore_mock):
    """
    Mock a firestore transaction with default values mimicking google.cloud.firestore.Transaction.
    This is required as MockFirestore does not support transactions mocking, and this set up enables
    unit-test without patching the transaction functions
    """
    mock_transaction = Mock(spec=Transaction)
    mock_transaction._read_only = False
    mock_transaction._max_attempts = 1
    mock_transaction._id = None
    firestore_mock.set_transaction.return_value = mock_transaction

    yield mock_transaction


@pytest.fixture(autouse=True)
def schema_collection_mock(firestore_mock):
    collection = firestore_mock.client.collection('schemas')
    firestore_mock.schemas_collection = collection
    firestore_mock.get_schemas_collection.return_value = collection

    yield collection


@pytest.fixture(autouse=True)
def dataset_collection_mock(firestore_mock):
    collection = firestore_mock.client.collection('datasets')
    firestore_mock.datasets_collection = collection
    firestore_mock.get_datasets_collection.return_value = collection

    yield collection


@pytest.fixture(autouse=True)
def deletion_collection_mock(firestore_mock):
    collection = firestore_mock.client.collection('marked_for_deletion')
    firestore_mock.deletion_collection = collection
    firestore_mock.get_deletion_collection.return_value = collection

    yield collection


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


@pytest.fixture
def dataset_service_with_repositories():
    """Create DatasetService with mocked repositories for unit tests."""
    dataset_storage_repository = MagicMock()
    dataset_deletion_repository = MagicMock()
    service = DatasetService(
        dataset_deletion_repository=dataset_deletion_repository,
        dataset_storage_repository=dataset_storage_repository,
    )

    return service, dataset_storage_repository, dataset_deletion_repository


@pytest.fixture
def schema_service_with_dependencies():
    """Create SchemaService with mocked repository and publisher dependencies."""
    schema_repository = MagicMock()
    publisher_service = MagicMock()
    service = SchemaService(
        schema_repository=schema_repository,
        publisher_service=publisher_service,
    )

    return service, schema_repository, publisher_service


@pytest.fixture
def publisher_service_factory():
    """Build PublisherService with mocked client and temporary settings patch."""

    def _factory(conf="unit"):
        publisher_client = MagicMock()
        publisher_client.topic_path.return_value = "projects/mock/topics/mock-topic"
        publisher_client.get_topic.return_value = MagicMock()

        with patch("app.services.shared.publisher_service.settings") as mock_settings:
            mock_settings.PROJECT_ID = "mock-project"
            mock_settings.PUBLISH_SCHEMA_TOPIC_ID = "mock-topic"
            mock_settings.CONF = conf
            service = PublisherService(publisher_client)

        return service, publisher_client

    return _factory


@pytest.fixture
def mock_http_response():
    """Build mocked HTTP responses with status code and json payload."""

    def _factory(status_code, json_data):
        response = Mock(spec=requests.Response)
        response.status_code = status_code
        response.json.return_value = json_data
        return response

    return _factory


