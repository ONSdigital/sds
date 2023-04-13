import logging
from unittest.mock import MagicMock, patch


def test_get_schema_200_is_logged(caplog, client, database):
    """
    When the schema is retrieved successfully there should be a log before and after.
    """
    caplog.set_level(logging.INFO)

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
    assert len(caplog.records) == 4
    assert caplog.records[0].message == "Getting schema metadata..."
    assert caplog.records[1].message == "Schema metadata successfully retrieved."
    assert caplog.records[2].message == "Getting schema..."
    assert caplog.records[3].message == "Schema successfully retrieved."


def test_get_schema_input_debug_logged(caplog, client, database):
    """
    When the schema is retrieved successfully there should be a log before and after.
    """
    caplog.set_level(logging.DEBUG)

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

    client.get("/v1/schema?survey_id=xyz&version=2")

    assert caplog.records[2].message == "Input data: survey_id=xyz, version=2"
    assert (
        caplog.records[4].message
        == "Schema metadata: SchemaMetadata(survey_id='xyz', schema_location='/xyz/111-222-xxx-fff.json', sds_schema_version=2, sds_published_at='2023-02-06T13:33:44Z')"
    )
    assert caplog.records[7].message == "Schema: {'hello': 'json'}"


@patch("database.get_schema_metadata")
def test_get_schema_404_is_logged(get_schema_metadata_mock, caplog, client):
    """
    When the schema metadata retrieval fails there should be an error log.
    """
    caplog.set_level(logging.ERROR)

    get_schema_metadata_mock.return_value = None
    response = client.get("/v1/schema?survey_id=xzy&version=2")

    assert response.status_code == 404
    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Schema metadata not found"
