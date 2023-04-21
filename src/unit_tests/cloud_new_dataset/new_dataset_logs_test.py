import logging
from unittest.mock import MagicMock, patch

cloud_event_test_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_name.json",
}

cloud_event_test_invalid_file = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_name.pdf",
}


@patch("dataset_storage.get_dataset")
@patch("database.set_dataset")
def test_new_dataset_info_is_logged(
    dataset_storage_mock,
    set_dataset_mock,
    caplog,
    cloud_functions,
):
    """
    There should be a log for when the cloud function is triggered and when the
    new dataset is successfully uploaded.
    """
    caplog.set_level(logging.INFO)

    dataset_storage_mock.return_value = {
        "survey_id": "xyz",
        "period_id": "abc",
        "form_type": "yyy",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
    }
    set_dataset_mock.return_value = {}

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    cloud_functions.new_dataset(cloud_event=cloud_event)

    assert len(caplog.records) == 3
    assert caplog.records[0].message == "Uploading new dataset..."
    assert caplog.records[1].message == "Dataset obtained successfully."
    assert caplog.records[2].message == "Dataset uploaded successfully."


@patch("dataset_storage.get_dataset")
@patch("database.set_dataset")
def test_new_dataset_debug_log(
    set_dataset_mock,
    dataset_storage_mock,
    caplog,
    cloud_functions,
):
    """
    There should be debug logs for inputted and retrieved data.
    """
    caplog.set_level(logging.DEBUG)

    dataset_storage_mock.return_value = {
        "survey_id": "xyz",
        "period_id": "abc",
        "form_type": "yyy",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
    }

    set_dataset_mock.return_value = {"hello": "world"}

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    cloud_functions.new_dataset(cloud_event=cloud_event)

    assert (
        caplog.records[1].message
        == "Cloud event data: {'id': 'test_id', 'type': 'test_type', 'bucket': "
        "'test_bucket', 'metageneration': '1', 'timeCreated': 'test_time_created', "
        "'updated': 'test_time_updated', 'name': 'test_name.json'}"
    )
    assert caplog.records[3].message == "Dataset: " + str(
        dataset_storage_mock.return_value
    )


def test_new_dataset_invalid_file(
    caplog,
    cloud_functions,
):
    """
    This test ensures that there is an error log when the filetype is invalid.
    """
    caplog.set_level(logging.ERROR)

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_invalid_file

    cloud_functions.new_dataset(cloud_event=cloud_event)

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Invalid filetype received - test_name.pdf"


@patch("dataset_storage.validate_keys")
def test_new_dataset_missing_keys(
    dataset_storage_mock,
    caplog,
    cloud_functions,
):
    """
    This test ensures that there are error logs when the mandatory keys are missing in the JSON file contents.
    """
    caplog.set_level(logging.ERROR)

    dataset_storage_mock.return_value = [False, "survey_id, period_id"]

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    cloud_functions.new_dataset(cloud_event=cloud_event)

    assert len(caplog.records) == 2
    assert (
        caplog.records[0].message
        == "The mandatory key(s) survey_id, period_id is/are missing in the JSON object."
    )
    assert caplog.records[1].message == "Invalid JSON file contents."
