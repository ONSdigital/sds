from unittest.mock import MagicMock

import firebase_admin
import pytest
from fastapi.testclient import TestClient
from firebase_admin import firestore


@pytest.fixture
def database(monkeypatch):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())
    import database

    yield database


@pytest.fixture
def client(database):
    import app

    app.database = database
    client = TestClient(app.app)
    yield client
