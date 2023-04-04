import json
from datetime import datetime


def test_dataset(client, bucket_loader):
    """
    Test that we can upload a dataset and then retrieve the data. This checks the cloud function worked.

    * We load the sample dataset json file
    * Generate a dataset_id which is guaranteed to be unique
    * Upload the dataset file to the dataset bucket with the dataset_id as the name
    * We then use the API to get some unit data back using the dataset_id and a known ru_ref
    """
    with open("../test_data/dataset.json") as f:
        dataset = json.load(f)

    # The dataset id an auto generated GUID and the filename is a field in the dataset metadata
    filename_id = f"integration-test-{str(datetime.now()).replace(' ','-')}"
    filename = f"{filename_id}.json"
    bucket_loader(filename, dataset)

    survey_id = "xyz"
    period_id = "abc"
    unit_id = "43532"

    dataset_metadata_response = client.get(
        f"/v1/dataset_metadata?survey_id={survey_id}&period_id={period_id}"
    )
    assert dataset_metadata_response.status_code == 200

    # Since the cloud function generates the GUID which is set as the dataset id, the below looping is necessary to
    # locate the specific dataset in the collection.
    # Iterate over all the items in the above API response, then locate the document with the "filename" field from above.
    for guid, integration_dataset in dataset_metadata_response.json()[
        "supplementary_dataset"
    ].items():
        if (
            dataset_metadata_response.json()["supplementary_dataset"][guid]["filename"]
            == filename
        ):
            dataset_id = guid

            response = client.get(
                f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}"
            )

            assert response.status_code == 200
            # Check that the API response is the same as the dataset just located in the loop
            assert response.json() == integration_dataset

            dataset_metadata = dataset_metadata_response.json()[
                "supplementary_dataset"
            ][guid]

            assert "sds_dataset_version" in dataset_metadata
            # Check that the "filename" attribute exists
            assert "filename" in dataset_metadata


def test_publish_schema(client):
    """
    Post a schema using the /schema api endpoint and check the metadata
    can be retrieved. Also check that schema can be retrieved directly from storage.
    """
    survey_id = "068"
    with open("../test_data/schema.json") as f:
        test_schema = json.load(f)

    response = client.post("/v1/schema", json=test_schema)
    assert response.status_code == 200

    response = client.get(f"/v1/schema_metadata?survey_id={test_schema['survey_id']}")
    assert response.status_code == 200

    json_response = response.json()
    assert len(json_response) > 0

    for schema in json_response:
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
