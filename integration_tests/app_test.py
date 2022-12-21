import json

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_publish():
    with open("data/data_set.json") as f:
        dataset = json.load(f)
    response = client.put("/publish", json=dataset)
    print(response.text)
    assert response.status_code == 200


def test_retrieve():
    data_set_id = "c2299a49-dfad-40d4-ba3a-7e94304c7cf6"
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = client.get(f"/unit_data?data_set_id={data_set_id}&unit_id={unit_id}")
    print(response.text)
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
