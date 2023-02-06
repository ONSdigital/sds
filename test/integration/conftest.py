import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    os.environ["FIREBASE_KEYFILE_LOCATION"] = "../firebase_key.json"
    from app import app

    client = TestClient(app)
    yield client


@pytest.fixture
def database():
    os.environ["FIREBASE_KEYFILE_LOCATION"] = "../firebase_key.json"
    import database

    yield database
