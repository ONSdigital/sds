import logging
from unittest.mock import MagicMock, patch


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
    dataset_storage_mock.return_value = {}
    set_dataset_mock.return_value = {}
    cloud_event = MagicMock()
    cloud_event.data = {
        "id": "test_id",
        "type": "test_type",
        "bucket": "test_bucket",
        "metageneration": "1",
        "timeCreated": "test_time_created",
        "updated": "test_time_updated",
        "name": "test_name.json",
    }

    cloud_functions.new_dataset(cloud_event=cloud_event)

    assert len(caplog.records) == 2
    assert caplog.records[0].message == "Uploading new dataset..."
    assert caplog.records[1].message == "Dataset successfully uploaded."


@patch("dataset_storage.get_dataset")
@patch("database.set_dataset")
def test_new_dataset_debug_log(
    dataset_storage_mock,
    set_dataset_mock,
    caplog,
    cloud_functions,
):
    """
    There should be a debug log containing the event data.
    """
    caplog.set_level(logging.DEBUG)
    dataset_storage_mock.return_value = {}
    set_dataset_mock.return_value = {}
    cloud_event = MagicMock()
    cloud_event.data = {
        "id": "test_id",
        "type": "test_type",
        "bucket": "test_bucket",
        "metageneration": "1",
        "timeCreated": "test_time_created",
        "updated": "test_time_updated",
        "name": "test_name.json",
    }

    cloud_functions.new_dataset(cloud_event=cloud_event)

    assert caplog.records[1].message == "Cloud event data: {'id': 'test_id', 'type': 'test_type', 'bucket': " \
                                        "'test_bucket', 'metageneration': '1', 'timeCreated': 'test_time_created', " \
                                        "'updated': 'test_time_updated', 'name': 'test_name.json'}"
