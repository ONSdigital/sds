import requests
import json
import os

CLOUD_RUN_ENDPOINT = os.environ.get("CLOUD_RUN_ENDPOINT")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}


def test_dataset():
    """
    Test that SDS runs on Cloud Run. To run this test, you will need to set the following environment
    variables:
    * CLOUD_RUN_ENDPOINT - get the URL from the cloud run console
    * AUTH_TOKEN - get this by running "gcloud auth print-identity-token"
    """
    with open("data/dataset.json") as f:
        dataset = json.load(f)
    response = requests.post(
        f"{CLOUD_RUN_ENDPOINT}/dataset", json=dataset, headers=headers
    )
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    response = requests.get(
        f"{CLOUD_RUN_ENDPOINT}/unit_data?dataset_id={dataset_id}&unit_id={unit_id}",
        headers=headers,
    )
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
