import json
from unittest.mock import MagicMock


def test_post_dataset(client):
    response = client.post("/dataset", json={"data": {}})
    dataset_id = response.json()["dataset_id"]
    assert response.status_code == 200
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_get_unit_data(client):
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    dataset_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_post_dataset_schema(client, database):
    """
    Checks that fastAPI accepts a valid schema file
    and returns a valid schema metadata file.
    """
    with open("../test_data/schema.json") as f:
        schema = json.load(f)
    response = client.post("/v1/schema", json=schema)
    assert response.status_code == 200
    schema_meta_data = response.json()
    assert schema_meta_data == {
        "survey_id": "xyz",
        "schema_location": schema_meta_data["schema_location"],
        "sds_schema_version": schema_meta_data["sds_schema_version"],
        "sds_published_at": schema_meta_data["sds_published_at"],
    }


def test_query_schemas(client, database):
    """
    Checks that query_schemas calls the get_schemas function in
    the database module and returns the returned dictionary.
    Furthermore, it checks that the FAST API response model
    is set up properly, as it should only allow through a valid schema_meta_data
    structure (like the example below).
    """
    expected_schema = {
        "survey_id": "xyz",
        "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
        "sds_schema_version": 1,
        "sds_published_at": "2023-02-06T13:33:44Z",
    }
    schema_guid = "abc"
    mock_stream_obj = MagicMock()
    mock_stream_obj.to_dict.return_value = expected_schema
    mock_stream_obj.id = schema_guid
    database.schemas_collection.where().stream.return_value = [mock_stream_obj]
    response = client.get("/v1/schema_metadata?survey_id=xzy")
    assert response.status_code == 200
    assert (
        response.json()["supplementary_dataset_schema"][schema_guid] == expected_schema
    )


def test_get_datasets(client):
    survey_id = "Survey 1"
    response = client.get(f"/datasets?&survey_id={survey_id}")
    assert response.status_code == 200
