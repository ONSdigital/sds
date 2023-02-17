import json
import os

import pytest
import requests
from fastapi.testclient import TestClient

KEYFILE_LOCATION = "../../key.json"
FIRESTORE_EMULATOR_HOST = "localhost:8200"


@pytest.fixture
def storage():
    import storage

    yield storage


@pytest.fixture
def database():
    """
    This database fixture will auto-switch between the firestore emulator
    and the real Firestore, depending on whether firebase_key.json present.
    If this file is not present and the emulator is not running it will fail
    with a useful message.
    """
    if os.path.exists(KEYFILE_LOCATION):
        os.environ["KEYFILE_LOCATION"] = KEYFILE_LOCATION
    else:
        try:
            requests.get(f"http://{FIRESTORE_EMULATOR_HOST}", timeout=0.1)
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
def client(database):
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


def test_publish_schema(client, storage):
    """
    Post a schema using the /schema api endpoint and check the metadata
    can retrieved. Also check that schema can be retrieved directly from storage.
    """
    survey_id = "xyz"
    with open("../test_data/schema.json") as f:
        test_schema = json.load(f)
    response = client.post("/v1/schema", json=test_schema)
    print(response.text)
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
        assert storage.get_schema(f"{survey_id}/{guid}.json") == test_schema
