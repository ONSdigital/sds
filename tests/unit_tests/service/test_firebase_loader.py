from unittest.mock import MagicMock, call

from app.util.firebase_loader import FirebaseLoader


def _make_firebase_loader() -> tuple[FirebaseLoader, MagicMock]:
    """Helper: build a FirebaseLoader backed by a mocked Firestore client."""
    mock_client = MagicMock()
    mock_client.collection.side_effect = lambda name: MagicMock(name=name)
    loader = FirebaseLoader(mock_client)
    return loader, mock_client


def test_firebase_loader_init_creates_all_three_collections():
    """
    FirebaseLoader.__init__ must create collection references for
    'datasets', 'schemas', and 'marked_for_deletion'.
    """
    loader, mock_client = _make_firebase_loader()

    mock_client.collection.assert_any_call("datasets")
    mock_client.collection.assert_any_call("schemas")
    mock_client.collection.assert_any_call("marked_for_deletion")


def test_get_client_returns_firestore_client():
    """
    get_client must return the Firestore client passed during initialisation.
    """
    loader, mock_client = _make_firebase_loader()

    assert loader.get_client() is mock_client


def test_get_datasets_collection_returns_datasets_collection():
    """
    get_datasets_collection must return the datasets CollectionReference.
    """
    loader, _ = _make_firebase_loader()

    result = loader.get_datasets_collection()

    assert result is loader.datasets_collection


def test_get_schemas_collection_returns_schemas_collection():
    """
    get_schemas_collection must return the schemas CollectionReference.
    """
    loader, _ = _make_firebase_loader()

    result = loader.get_schemas_collection()

    assert result is loader.schemas_collection


def test_get_deletion_collection_returns_deletion_collection():
    """
    get_deletion_collection must return the marked_for_deletion CollectionReference.
    """
    loader, _ = _make_firebase_loader()

    result = loader.get_deletion_collection()

    assert result is loader.deletion_collection


def test_set_transaction_returns_client_transaction():
    """
    set_transaction must call client.transaction() and return its result.
    """
    loader, mock_client = _make_firebase_loader()
    mock_transaction = MagicMock()
    mock_client.transaction.return_value = mock_transaction

    result = loader.set_transaction()

    mock_client.transaction.assert_called_once()
    assert result is mock_transaction

