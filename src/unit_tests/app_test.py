from unittest.mock import MagicMock

import firebase_admin
import pytest
from fastapi.testclient import TestClient
from firebase_admin import firestore
import json


@pytest.fixture
def database():
    database = MagicMock()
    yield database


@pytest.fixture
def client(database, monkeypatch):
    monkeypatch.setattr(firebase_admin, "credentials", MagicMock())
    monkeypatch.setattr(firebase_admin, "initialize_app", MagicMock())
    monkeypatch.setattr(firestore, "client", MagicMock())
    import app

    app.database = database
    client = TestClient(app.app)
    yield client


def test_post_dataset(client):
    response = client.post("/dataset", json={"data": {}})
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_get_unit_data(client):
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    dataset_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_post_dataset_schema(client, database):
    schema_meta_data = {
        "survey_id": "xxx",
        "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
        "sds_schema_version": 1,
        "sds_published_at": "2023-02-06T13:33:44Z",
    }
    database.set_schema_metadata.return_value = schema_meta_data
    with open("test_schema.json") as f:
        schema = json.load(f)
    response = client.post("/v1/schema", json=schema)
    assert response.status_code == 200
    assert response.json() == schema_meta_data
    assert database.set_schema_metadata.call_args[1] == {
        "survey_id": "xxx",
        "schema_location": "/",
    }


def test_get_dataset_schema(client):
    dataset_schema_id = "sppi_dataset_schema"
    version = "1"
    response = client.get(
        f"/dataset_schema?dataset_schema_id={dataset_schema_id}&version={version}"
    )
    assert response.status_code == 200


def test_query_schemas(client, database):
    """
    Checks that query_schemas calls the get_schemas function in
    the database module and returns the returned dictionary.
    Furthermore, it checks that the FAST API response model
    is set up properly, as it should only allow through a valid schema_meta_data
    structure (like the example below).
    """
    get_schemas = database.get_schemas
    schema_meta_data = {
        "supplementary_dataset_schema": {
            "111-222-xxx-fff": {
                "survey_id": "xxx",
                "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
                "sds_schema_version": 1,
                "sds_published_at": "2023-02-06T13:33:44Z",
            }
        }
    }
    database.get_schemas.return_value = schema_meta_data
    survey_id = "Survey 1"
    response = client.get(f"/v1/schema_metadata?survey_id={survey_id}")
    assert response.status_code == 200
    assert response.json() == schema_meta_data
    database.get_schemas = get_schemas


def test_get_datasets(client):
    survey_id = "Survey 1"
    response = client.get(f"/datasets?&survey_id={survey_id}")
    assert response.status_code == 200
