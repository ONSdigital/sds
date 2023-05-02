import json
from unittest.mock import MagicMock, patch

from config.config_factory import ConfigFactory

config = ConfigFactory.get_config()


@patch("uuid.uuid4")
def test_post_schema_metadata(mock_uuid, client, database, storage):
    """
    Checks that fastAPI accepts a valid schema file
    and returns a valid schema metadata file.
    """
    mock_uuid.return_value = "test-uuid"
    with open(config.TEST_SCHEMA_PATH) as f:
        schema = json.load(f)

    response = client.post("/v1/schema", json=schema)

    assert response.status_code == 200

    schema_meta_data = response.json()

    assert schema_meta_data == {
        "guid": mock_uuid.return_value,
        "survey_id": "076",
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
    Checks that fastAPI returns a 400 error if the schema
    is badly formatted.
    """
    response = client.post("/v1/schema", json={"schema": "is missing some fields"})
    assert response.status_code == 400


def test_get_schemas_metadata(client, database):
    """
    Checks that query_schemas calls the get_schemas function in
    the database module and returns the returned dictionary.
    Furthermore, it checks that the FAST API response model
    is set up properly, as it should only allow through a valid schema_meta_data
    structure (like the example below).
    """
    expected_schema = {
        "guid": "abc",
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
    assert expected_schema in response.json()


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
        "dataset_id": "abc-xyz",
        "survey_id": "xyz",
        "period_id": "abc",
        "title": "Which side was better?",
        "sds_schema_version": 4,
        "sds_dataset_version": 23,
        "sds_published_at": "2023-03-13T14:34:57Z",
        "total_reporting_units": 2,
        "schema_version": "v1.0.0",
        "form_type": "yyy",
        "filename": "file1.json",
    }
    dataset_id = "abc-xyz"
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
    assert response.json()[0] == expected_metadata


def test_get_metadata_metadata_with_invalid_version_error(client):
    """
    Checks that fastAPI does not accept invalid porameters/
    non-numeric version and returns a 400 error with appropriate message at
    dataset_metadata endpoint
    """
    response = client.get("/v1/schema?survey_id=076&version=xyz")

    assert response.status_code == 400
    assert response.json()["message"] == "Validation has failed"


def test_get_dataset_metadata_with_not_found_error(client):
    """
    Checks that fastAPI return 404 error with apppropriate msg
    when dataset metadata is not found at dataset metadata
    endpoint
    """
    response = client.get("/v1/schema_metadata?survey_id=123")

    assert response.status_code == 404
    assert response.json()["message"] == "No results found"


def test_get_unit_data_with_not_found_error(client):
    """
    Checks that fastAPI return 404 error with apppropriate msg
    when unit data is not found
    """
    response = client.get("/v1/schema_metadata?survey_id=123")

    assert response.status_code == 404
    assert response.json()["message"] == "No results found"

