import logging
from unittest.mock import patch

dataset_metadata_collection_test_data = [
    {
        "dataset_id": "test_dataset_id",
        "survey_id": "test_survey_id",
        "period_id": "test_period_id",
        "title": "test_title",
        "sds_schema_version": 1,
        "sds_published_at": "test_published_at",
        "total_reporting_units": 1,
        "schema_version": "test_version",
        "sds_dataset_version": 1,
        "filename": "test_filename",
        "form_type": "test_form_type",
    }
]


@patch("database.get_dataset_metadata_collection")
def test_get_dataset_metadata_collection_200_is_logged(
    get_dataset_metadata_collection_mock, caplog, client
):
    """
    When the schema metadata is retrieved successfully there should be a log before and after.
    """
    caplog.set_level(logging.INFO)

    get_dataset_metadata_collection_mock.return_value = (
        dataset_metadata_collection_test_data
    )
    response = client.get("/v1/dataset_metadata?survey_id=xzy&period_id=abc")

    assert response.status_code == 200
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Getting dataset metadata collection..."
    assert (
        caplog.records[1].message
        == "Dataset metadata collection successfully retrieved."
    )


@patch("database.get_dataset_metadata_collection")
def test_get_dataset_metadata_collection_404_is_logged(
    get_dataset_metadata_collection_mock, caplog, client
):
    """
    When no data is retrieved there should be an error log.
    """
    caplog.set_level(logging.ERROR)

    get_dataset_metadata_collection_mock.return_value = None
    response = client.get("/v1/dataset_metadata?survey_id=xzy&period_id=abc")

    assert response.status_code == 404
    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Dataset metadata collection not found."


@patch("database.get_dataset_metadata_collection")
def test_get_dataset_metadata_collection_debug_logs(
    get_dataset_metadata_collection_mock, caplog, client
):
    """
    There should be debug logs for data inputted and retrieved.
    """
    caplog.set_level(logging.DEBUG)

    get_dataset_metadata_collection_mock.return_value = (
        dataset_metadata_collection_test_data
    )
    client.get("/v1/dataset_metadata?survey_id=xyz&period_id=abc")

    assert caplog.records[2].message == "Input data: survey_id=xyz, period_id=abc"
    assert (
        caplog.records[4].message
        == "Dataset metadata collection: [{'dataset_id': 'test_dataset_id', 'survey_id': "
        "'test_survey_id', 'period_id': 'test_period_id', 'title': 'test_title', "
        "'sds_schema_version': 1, 'sds_published_at': 'test_published_at', "
        "'total_reporting_units': 1, 'schema_version': 'test_version', "
        "'sds_dataset_version': 1, 'filename': 'test_filename', 'form_type': "
        "'test_form_type'}]"
    )
