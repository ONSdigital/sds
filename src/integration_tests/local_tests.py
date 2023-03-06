import json
import os
import uuid
from time import sleep

import pytest
import requests
from fastapi.testclient import TestClient
from google.cloud import storage as gcp_storage

KEYFILE_LOCATION = "../../key.json"
FIRESTORE_EMULATOR_HOST = "localhost:8200"
STORAGE_EMULATOR_HOST = "http://localhost:9023"
DATASET_BUCKET = os.environ.get("DATASET_BUCKET")

storage_client = gcp_storage.Client()

bucket = storage_client.bucket(DATASET_BUCKET)


@pytest.fixture
def storage():
    """
    This storage fixture will auto-switch between the emulator
    and the real thing, depending on whether key.json present.
    """
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
    dataset_id = str(uuid.uuid4())
    filename = f"{dataset_id}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(dataset, indent=2), content_type="application/json"
    )
    unit_id = "43532"
    sleep(2)
    response = client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")
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
