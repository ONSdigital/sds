import json
from time import sleep
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
    dataset_id = f"integration-test-{str(datetime.now()).replace(' ','-')}"
    print(dataset_id)
    filename = f"{dataset_id}.json"
    bucket_loader(filename, dataset)
    unit_id = "43532"
    sleep(3)
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
    survey_id = "068"
    with open("../test_data/schema.json") as f:
        test_schema = json.load(f)
    response = client.post("/v1/schema", json=test_schema)
    print(response.text)
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
