import json

from fastapi.testclient import TestClient
import os

os.environ["FIREBASE_KEYFILE_LOCATION"] = "../firebase_key.json"
from app import app

client = TestClient(app)


def test_data_set():
    with open("data/data_set.json") as f:
        dataset = json.load(f)
    response = client.post("/data_set", json=dataset)
    data_set_id = response.json()["data_set_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = client.get(f"/unit_data?data_set_id={data_set_id}&unit_id={unit_id}")
    assert response.status_code == 200
    assert response.json() == {
        "unit_id": "55e64129-6acd-438b-a23a-3cf9524ab912",
        "title": "SPPI supplementary data set",
        "description": "supplementary data for SPPI Survey",
        "type": "object",
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


def test_schema():
    with open("data/schema.json") as f:
        schema = json.load(f)
    response = client.post("/schema", json=schema)
    schema_id = response.json()["schema_id"]
    assert response.status_code == 200
    response = client.get(f"/schema?schema_id={schema_id}")
    assert response.status_code == 200
    assert response.json() == schema
