import json
import os

from fastapi.testclient import TestClient

os.environ["FIREBASE_KEYFILE_LOCATION"] = "../firebase_key.json"
from app import app

client = TestClient(app)


def test_dataset():
    with open("data/dataset.json") as f:
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


def test_dataset_design():
    with open("data/schema.json") as f:
        schema = json.load(f)
    dataset_design_id = "sppi_dataset_design"
    response = client.post(
        f"/dataset_design?dataset_design_id={dataset_design_id}", json=schema
    )
    version = response.json()["version"]
    assert response.status_code == 200
    response = client.get(
        f"/dataset_design?dataset_design_id={dataset_design_id}&version={version}"
    )
    assert response.status_code == 200
    assert response.json() == schema
