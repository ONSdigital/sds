import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    from app import app

    test_client = TestClient(app)

    yield test_client
