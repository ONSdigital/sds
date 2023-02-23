import json
import os

import pytest
import requests
from fastapi.testclient import TestClient

KEYFILE_LOCATION = "../../key.json"
FIRESTORE_EMULATOR_HOST = "localhost:8200"
STORAGE_EMULATOR_HOST = "http://localhost:9023"


@pytest.fixture
def storage():
    """
    This storage fixture will auto-switch between the emulator
    and the real thing, depending on whether key.json present.
    """
    server = None
    if os.path.exists(KEYFILE_LOCATION):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEYFILE_LOCATION
    else:
        try:
            requests.get(STORAGE_EMULATOR_HOST, timeout=5)
        except requests.exceptions.ConnectionError:
            pytest.fail(
                "You need to run the Firestore emulator or fill "
                "in firebase_key.json with creds for a real"
                "database instance."
            )
        os.environ["STORAGE_EMULATOR_HOST"] = STORAGE_EMULATOR_HOST
        os.environ["SCHEMA_BUCKET_NAME"] = "bucket"
    import storage

    yield storage
    if server:
        server.stop()


@pytest.fixture
def database():
    """
    This database fixture will auto-switch between the firestore emulator
    and the real Firestore, depending on whether key.json present.
    If this file is not present and the emulator is not running it will fail
    with a useful message.
    """
    if os.path.exists(KEYFILE_LOCATION):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEYFILE_LOCATION
    else:
        try:
            requests.get(f"http://{FIRESTORE_EMULATOR_HOST}", timeout=5)
        except requests.exceptions.ConnectionError:
            pytest.fail(
                "You need to run the Firestore emulator or fill "
                "in firebase_key.json with creds for a real"
                "database instance."
            )
        os.environ["FIRESTORE_EMULATOR_HOST"] = FIRESTORE_EMULATOR_HOST
    import database

    yield database


@pytest.fixture
def client(database, storage):
    from app import app

    client = TestClient(app)
    yield client


def test_dataset(client):
    with open("../test_data/dataset.json") as f:
        dataset = json.load(f)
    response = client.post("/dataset", json=dataset)
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")
    assert response.status_code == 200
    assert response.json() == {
        "unit_id": "55e64129-6acd-438b-a23a-3cf9524ab912",
        "properties": {
            "sample_unit": {
                "units_of_sale": "MILES MAPPED",
                "currency_description": "SILVER COINS",
                "time_items": [
                    {"ref": "M1", "grade": "Chief mapper"},
                    {"ref": "M2", "grade": "Junior mapper"},
                    {"ref": "M3", "grade": "Bag carrier"},
                ],
            }
        },
    }


def test_publish_schema(client):
    """
    Post a schema using the /schema api endpoint and check the metadata
    can retrieved. Also check that schema can be retrieved directly from storage.
    """
    survey_id = "xyz"
    with open("../test_data/schema.json") as f:
        test_schema = json.load(f)
    response = client.post("/v1/schema", json=test_schema)
    assert response.status_code == 200
    response = client.get(f"/v1/schema_metadata?survey_id={test_schema['survey_id']}")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["supplementary_dataset_schema"]) > 0
    for guid, schema in json_response["supplementary_dataset_schema"].items():
        assert schema == {
            "survey_id": survey_id,
            "schema_location": f"{survey_id}/{guid}.json",
            "sds_schema_version": schema["sds_schema_version"],
            "sds_published_at": schema["sds_published_at"],
        }
        response = client.get(
            f"/v1/schema?survey_id={schema['survey_id']}&version={schema['sds_schema_version']}"
        )
        assert response.status_code == 200
        assert response.json() == test_schema
