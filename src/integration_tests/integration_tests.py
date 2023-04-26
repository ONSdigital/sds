import json
from datetime import datetime

from config.config_factory import ConfigFactory

config = ConfigFactory.get_config()


def test_dataset(client, bucket_loader):
    """
    Test that we can upload a dataset and then retrieve the data. This checks the cloud function worked.

    * We load the sample dataset json file
    * Upload the dataset file to the dataset bucket with the dataset_id as the name
    * We then use the API to get some unit data back using the dataset_id and a known ru_ref
    * The dataset id an auto generated GUID
    """
    with open(config.TEST_DATASET_PATH) as f:
        dataset = json.load(f)

    filename_id = f"integration-test-{str(datetime.now()).replace(' ','-')}"
    filename = f"{filename_id}.json"
    bucket_loader(filename, dataset)

    survey_id = "xyz"
    period_id = "abc"

    dataset_metadata_response = client.get(
        f"/v1/dataset_metadata?survey_id={survey_id}&period_id={period_id}"
    )
    assert dataset_metadata_response.status_code == 200

    mock_unit_response = {
        "schema_version": "v1.0.0",
        "sds_schema_version": 4,
        "survey_id": "xyz",
        "period_id": "abc",
        "form_type": "yyy",
        "data": {
            "busdesc": "Provision of equipment for hobbit adventures",
            "local_unit": [
                {
                    "luaddr2": "Underhill",
                    "luref": "2012763A",
                    "busdesc": "Creates old fashioned looking paper maps",
                    "luname": "Maps Factory",
                    "luaddr1": "1 Bag End",
                    "tradstyle": "Also Does Adventures Ltd",
                    "luaddr3": "Hobbiton",
                    "lupostcode": "HO1 1AA",
                },
                {
                    "luaddr2": "Maggotsville",
                    "luref": "20127364B",
                    "busdesc": "Quality pipe manufacturer",
                    "buslref": "pipe123",
                    "luname": "Pipes R Us Subsidiary",
                    "luaddr1": "12 The Farmstead",
                    "luaddr3": "Hobbiton",
                    "lupostcode": "HO1 1AB",
                },
            ],
            "payeref": "123AB456",
            "runame": "Pipes and Maps Ltd",
            "rupostcode": "HO1 1AA",
            "ruaddr1": "111 Under Hill",
            "ruaddr4": "The Shire",
            "ruaddr2": "Hobbitton",
            "ruref": "43532",
        }
    }
    # Since the cloud function generates the GUID which is set as the dataset id, the below looping is necessary to
    # locate the specific dataset in the collection.
    # Iterate over all the items in the above API response, then locate the document with the "filename" field from above.

    for dataset_metadata in dataset_metadata_response.json():
        if dataset_metadata["filename"] == filename:
            dataset_id = dataset_metadata["dataset_id"]
            unit_id = "43532"

            response = client.get(
                f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}"
            )

            assert response.status_code == 200
            assert mock_unit_response.items() <= response.json().items()

            assert "sds_dataset_version" in dataset_metadata
            assert "filename" in dataset_metadata
            assert "form_type" in dataset_metadata


def test_post_schema(client):
    """
    Post a schema using the /schema api endpoint and check the metadata
    can be retrieved. Also check that schema can be retrieved directly from storage.
    """
    survey_id = "076"
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
