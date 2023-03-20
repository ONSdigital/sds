import json
from unittest.mock import MagicMock


def test_get_unit_data(client):
    unit_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    dataset_id = "55e64129-6acd-438b-a23a-3cf9524ab912"
    client.get(f"/v1/unit_data?dataset_id={dataset_id}&unit_id={unit_id}")


def test_post_dataset_schema(client, database, storage):
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
        "survey_id": "068",
        "schema_location": schema_meta_data["schema_location"],
        "sds_schema_version": schema_meta_data["sds_schema_version"],
        "sds_published_at": schema_meta_data["sds_published_at"],
    }
    schema_string = (
        storage.storage_client.bucket().blob().upload_from_string.call_args[0][0]
    )
    assert json.loads(schema_string) == schema


def test_post_bad_schema(client, database, storage):
    """
    Checks that fastAPI returns a 422 error if the schema
    is badly formatted.
    """
    response = client.post("/v1/schema", json={"schema": "is missing some fields"})
    assert response.status_code == 422


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


def test_get_schema(client, database):
    """
    Checks that we get schema metadata when we get the
    survey_id and version and that we use that to return
    the schema file from storage.
    """
    expected_metadata = {
        "survey_id": "xyz",
        "schema_location": "/xyz/111-222-xxx-fff.json",
        "sds_schema_version": 2,
        "sds_published_at": "2023-02-06T13:33:44Z",
    }
    schema_guid = "abc"
    mock_stream_obj = MagicMock()
    mock_stream_obj.to_dict.return_value = expected_metadata
    mock_stream_obj.id = schema_guid
    database.schemas_collection.where().where().stream.return_value = [mock_stream_obj]
    response = client.get("/v1/schema?survey_id=xzy&version=2")
    assert response.status_code == 200
    assert response.json() == {"hello": "json"}


def test_get_dataset_metadata(client, database):
    """
    Checks that the API endpoint '/v1/dataset_metadata' returns the expected dataset dictionary object
    when invoked with the survey_id and period_id parameters.
    """
    expected_metadata = {
        "survey_id": "xyz",
        "period_id": "abc",
        "title": "Which side was better?",
        "sds_schema_version": 4,
        "sds_dataset_version": 23,
        "sds_published_at": "2023-03-13T14:34:57Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "form_id": "yyy",
    }
    dataset_id = "wobble"
    mock_stream_obj = MagicMock()
    mock_stream_obj.to_dict.return_value = expected_metadata
    mock_stream_obj.id = dataset_id
    database.schemas_collection.where().where().stream.return_value = [mock_stream_obj]
    survey_id = "xyz"
    period_id = "abc"
    response = client.get(
        f"/v1/dataset_metadata?survey_id={survey_id}&period_id={period_id}"
    )
    assert response.status_code == 200
    assert response.json()["supplementary_dataset"][dataset_id] == expected_metadata
