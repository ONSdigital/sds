import json
from datetime import datetime

from config.config_factory import ConfigFactory

config = ConfigFactory.get_config()


def test_dataset(client, bucket_loader):
    """
    Test that we can upload a dataset and then retrieve the data. This checks the cloud function worked.

    * We load the sample dataset json file
    * Upload the dataset file to the dataset bucket twice
    * We then use the API to get some unit data back using the dataset_id and a known ru_ref
    * The dataset id is an auto generated GUID
    """
    with open(config.TEST_DATASET_PATH) as f:
        dataset = json.load(f)

    filename_id = f"integration-test-{str(datetime.now()).replace(' ','-')}"
    filename = f"{filename_id}.json"

    bucket_loader(filename, dataset)
    bucket_loader(filename, dataset)

    survey_id = "test_survey_id"
    period_id = "abc"

    dataset_metadata_response = client.get(
        f"/v1/dataset_metadata?survey_id={survey_id}&period_id={period_id}"
    )
    assert dataset_metadata_response.status_code == 200
    assert len(dataset_metadata_response.json()) == 1

    mock_unit_response = {
        "schema_version": "v1.0.0",
        "sds_schema_version": 4,
        "survey_id": "test_survey_id",
        "period_id": "abc",
        "data": "<encrypted data>",
    }

    for dataset_metadata in dataset_metadata_response.json():
        if dataset_metadata["filename"] == filename:
            dataset_id = dataset_metadata["dataset_id"]
            unit_id = "43532"

            response = client.get(
                f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}"
            )

            assert response.status_code == 200
            json_response = response.json()

            assert mock_unit_response.items() <= json_response.items()
            assert json_response["dataset_id"] is not None

            assert "sds_dataset_version" in dataset_metadata
            assert "filename" in dataset_metadata


def test_empty_bucket(bucket_loader):
    with open(config.TEST_DATASET_PATH) as f:
        dataset = json.load(f)

    filename_id = f"integration-test-{str(datetime.now()).replace(' ','-')}"
    filename = f"{filename_id}.json"

    bucket_loader(filename, dataset)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(config.DATASET_BUCKET_NAME)

    assert sum(1 for _ in bucket.list_blobs()) == 0


def test_post_schema(client):
    """
    Post a schema using the /schema api endpoint and check the metadata
    can be retrieved. Also check that schema can be retrieved directly from storage.
    """
    survey_id = "test_survey_id"
    with open(config.TEST_SCHEMA_PATH) as f:
        test_schema = json.load(f)

    schema_post_response = client.post("/v1/schema", json=test_schema)
    assert schema_post_response.status_code == 200
    assert "guid" in schema_post_response.text

    test_schema_get_response = client.get(
        f"/v1/schema_metadata?survey_id={test_schema['survey_id']}"
    )
    assert test_schema_get_response.status_code == 200

    response_as_json = test_schema_get_response.json()
    assert len(response_as_json) > 0

    for schema in response_as_json:
        assert schema == {
            "guid": schema["guid"],
            "survey_id": survey_id,
            "schema_location": f"{survey_id}/{schema['guid']}.json",
            "sds_schema_version": schema["sds_schema_version"],
            "sds_published_at": schema["sds_published_at"],
        }

        response = client.get(
            f"/v1/schema?survey_id={schema['survey_id']}&version={schema['sds_schema_version']}"
        )

        assert response.status_code == 200
        assert response.json() == test_schema
