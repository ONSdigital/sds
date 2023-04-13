import logging
from unittest.mock import patch

get_schemas_metadata_test_data = [
    {
        "guid": "abc",
        "survey_id": "xyz",
        "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
        "sds_schema_version": 1,
        "sds_published_at": "2023-02-06T13:33:44Z",
    }
]


@patch("database.get_schemas_metadata")
def test_get_schemas_metadata_200_is_logged(get_schemas_metadata_mock, caplog, client):
    """
    When the schema metadata is retrieved successfully there should be a log before and after.
    """
    caplog.set_level(logging.INFO)

    get_schemas_metadata_mock.return_value = get_schemas_metadata_test_data
    response = client.get("/v1/schema_metadata?survey_id=xzy")

    assert response.status_code == 200
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Getting schemas metadata..."
    assert caplog.records[1].message == "Schemas metadata successfully retrieved."


@patch("database.get_schemas_metadata")
def test_get_schemas_metadata_debug_logs(get_schemas_metadata_mock, caplog, client):
    """
    There should be debug logs for inputted and retrieved data.
    """
    caplog.set_level(logging.DEBUG)

    get_schemas_metadata_mock.return_value = get_schemas_metadata_test_data
    client.get("/v1/schema_metadata?survey_id=xyz")

    assert caplog.records[2].message == "Input data: survey_id=xyz"
    assert (
        caplog.records[4].message
        == "Schemas metadata: [{'guid': 'abc', 'survey_id': 'xyz', 'schema_location': "
        "'GC-BUCKET:/schema/111-222-xxx-fff.json', 'sds_schema_version': 1, 'sds_published_at': "
        "'2023-02-06T13:33:44Z'}]"
    )
