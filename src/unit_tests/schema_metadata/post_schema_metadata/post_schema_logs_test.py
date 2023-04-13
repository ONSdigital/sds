import logging
from unittest.mock import patch


@patch("services.schema_metadata_service.process_schema_metadata")
def test_post_schema_metadata_200_is_logged(process_mock, caplog, client):
    """
    When the schema metadata is posted successfully a message is logged.
    """
    caplog.set_level(logging.INFO)

    process_mock.return_value = {
        "guid": "test_guid",
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_at",
    }

    test_schema_metadata = {
        "$schema": "test-schema",
        "$id": "test-id",
        "survey_id": "100",
        "title": "test title",
        "description": "test description",
        "schema_version": "v1.0.0",
        "sample_unit_key_field": "test_ref",
        "properties": [],
        "examples": [],
    }

    response = client.post("/v1/schema", json=test_schema_metadata)

    assert response.status_code == 200
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Posting schema metadata..."
    assert caplog.records[1].message == "Schema metadata successfully posted."


@patch("services.schema_metadata_service.process_schema_metadata")
def test_post_schema_metadata_200_is_logged(process_mock, caplog, client):
    """
    When the schema metadata is posted successfully a message is logged.
    """
    caplog.set_level(logging.DEBUG)

    process_mock.return_value = {
        "guid": "test_guid",
        "survey_id": "test_survey_id",
        "schema_location": "test_schema_location",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_at",
    }

    test_schema_metadata = {
        "$schema": "test-schema",
        "$id": "test-id",
        "survey_id": "100",
        "title": "test title",
        "description": "test description",
        "schema_version": "v1.0.0",
        "sample_unit_key_field": "test_ref",
        "properties": [],
        "examples": [],
    }

    client.post("/v1/schema", json=test_schema_metadata)

    assert caplog.records[2].message == "Input body: {survey_id='100' title='test title' description='test " \
                                        "description' schema_version='v1.0.0' sample_unit_key_field='test_ref' " \
                                        "properties=[] examples=[] d_schema='test-schema' d_id='test-id'}"
    assert caplog.records[4].message == "Schema metadata: {'guid': 'test_guid', 'survey_id': 'test_survey_id', " \
                                        "'schema_location': 'test_schema_location', 'sds_schema_version': 1, " \
                                        "'sds_published_at': 'test_published_at'}"
