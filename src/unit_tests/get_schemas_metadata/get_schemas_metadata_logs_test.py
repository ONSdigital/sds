import logging
from unittest.mock import patch


@patch('database.get_schemas_metadata')
def test_get_schemas_metadata_200_is_logged(get_schemas_metadata_mock, caplog, client):
    """
    When the schema metadata is retrieved successfully there should be a log before and after.
    """
    caplog.set_level(logging.INFO)

    get_schemas_metadata_mock.return_value = [{
        "guid": "abc",
        "survey_id": "xyz",
        "schema_location": "GC-BUCKET:/schema/111-222-xxx-fff.json",
        "sds_schema_version": 1,
        "sds_published_at": "2023-02-06T13:33:44Z",
    }]
    response = client.get("/v1/schema_metadata?survey_id=xzy")

    assert response.status_code == 200
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Getting schemas metadata..."
    assert caplog.records[1].message == "Schemas metadata successfully retrieved."
