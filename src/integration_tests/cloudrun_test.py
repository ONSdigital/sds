import json
import os
import uuid
from time import sleep

import requests
from google.cloud import storage

storage_client = storage.Client()

DATASET_BUCKET = os.environ.get("DATASET_BUCKET")
bucket = storage_client.bucket(DATASET_BUCKET)

CLOUD_RUN_ENDPOINT = os.environ.get("CLOUD_RUN_ENDPOINT")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}


def test_dataset():
    with open("../test_data/dataset.json") as f:
        dataset = json.load(f)
    dataset_id = str(uuid.uuid4())
    filename = f"{dataset_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )
    unit_id = "43532"
    sleep(2)
    response = requests.get(
        f"{CLOUD_RUN_ENDPOINT}/unit_data?dataset_id={dataset_id}&unit_id={unit_id}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "ruref": "43532",
        "runame": "Pipes and Maps Ltd",
        "ruaddr1": "111 Under Hill",
        "ruaddr2": "Hobbitton",
        "ruaddr4": "The Shire",
        "rupostcode": "HO1 1AA",
        "payeref": "123AB456",
        "busdesc": "Provision of equipment for hobbit adventures",
        "local_unit": [
            {
                "luref": "2012763A",
                "luname": "Maps Factory",
                "luaddr1": "1 Bag End",
                "luaddr2": "Underhill",
                "luaddr3": "Hobbiton",
                "lupostcode": "HO1 1AA",
                "tradstyle": "Also Does Adventures Ltd",
                "busdesc": "Creates old fashioned looking paper maps",
            },
            {
                "luref": "20127364B",
                "luname": "Pipes R Us Subsidiary",
                "luaddr1": "12 The Farmstead",
                "luaddr2": "Maggotsville",
                "luaddr3": "Hobbiton",
                "lupostcode": "HO1 1AB",
                "busdesc": "Quality pipe manufacturer",
                "buslref": "pipe123",
            },
        ],
    }


def test_publish_schema():
    """
    Post a schema using the /schema api endpoint and check the metadata
    can retrieved. Also check that schema can be retrieved.
    """
    survey_id = "068"
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
        response = requests.get(
            f"{CLOUD_RUN_ENDPOINT}/v1/schema?survey_id={survey_id}&version={schema['sds_schema_version']}",
            headers=headers,
        )
        print(response.text)
        assert response.status_code == 200
        assert response.json() == test_schema
