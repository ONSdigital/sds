import os

import pytest
from fastapi.testclient import TestClient

FIREBASE_KEYFILE_LOCATION = "../../firebase_key.json"


@pytest.fixture
def client():
    os.environ["FIREBASE_KEYFILE_LOCATION"] = FIREBASE_KEYFILE_LOCATION
    from app import app

    client = TestClient(app)
    yield client


@pytest.fixture
def database():
    os.environ["FIREBASE_KEYFILE_LOCATION"] = FIREBASE_KEYFILE_LOCATION
    import database

    yield database
