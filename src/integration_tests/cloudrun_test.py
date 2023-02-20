import json
import os

import requests

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
    with open("../test_data/dataset.json") as f:
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


def test_publish_schema():
    """
    Post a schema using the /schema api endpoint and check the metadata
    can retrieved. Also check that schema can be retrieved directly from storage.
    """
    survey_id = "xyz"
    with open("../test_data/schema.json") as f:
        test_schema = json.load(f)
    response = requests.post(
        f"{CLOUD_RUN_ENDPOINT}/v1/schema", json=test_schema, headers=headers
    )
    print(response.text)
    assert response.status_code == 200
    response = requests.get(
        f"{CLOUD_RUN_ENDPOINT}/v1/schema_metadata?survey_id={test_schema['survey_id']}",
        headers=headers,
    )
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
