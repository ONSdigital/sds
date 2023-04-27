import logging
from unittest.mock import MagicMock

from bucket.bucket_file_reader import BucketFileReader
from services.dataset.dataset_processor_service import DatasetProcessorService

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


def test_new_dataset_info_is_logged(
    caplog,
    cloud_function,
):
    """
    There should be a log for when the cloud function is triggered and when the
    new dataset is successfully uploaded.
    """
    caplog.set_level(logging.INFO)

    BucketFileReader.get_file_from_bucket = MagicMock()
    DatasetProcessorService.process_new_dataset = MagicMock()

    BucketFileReader.get_file_from_bucket.return_value = {
        "survey_id": "xyz",
        "period_id": "abc",
        "form_type": "yyy",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
    }
    DatasetProcessorService.process_new_dataset.return_value = {}

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    cloud_function.new_dataset(cloud_event=cloud_event)

    assert len(caplog.records) == 3
    assert caplog.records[0].message == "Uploading new dataset..."
    assert caplog.records[1].message == "Dataset obtained successfully."
    assert caplog.records[2].message == "Dataset uploaded successfully."


def test_new_dataset_debug_log(
    caplog,
    cloud_function,
):
    """
    There should be debug logs for inputted and retrieved data.
    """
    caplog.set_level(logging.DEBUG)

    BucketFileReader.get_file_from_bucket = MagicMock()
    DatasetProcessorService.process_new_dataset = MagicMock()

    BucketFileReader.get_file_from_bucket.return_value = {
        "survey_id": "xyz",
        "period_id": "abc",
        "form_type": "yyy",
        "sds_schema_version": 4,
        "schema_version": "v1.0.0",
    }
    DatasetProcessorService.process_new_dataset.return_value = None

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    cloud_function.new_dataset(cloud_event=cloud_event)

    assert (
        caplog.records[1].message
        == "Cloud event data: {'id': 'test_id', 'type': 'test_type', 'bucket': "
        "'test_bucket', 'metageneration': '1', 'timeCreated': 'test_time_created', "
        "'updated': 'test_time_updated', 'name': 'test_name.json'}"
    )
    assert caplog.records[3].message == "Dataset: " + str(
        BucketFileReader.get_file_from_bucket.return_value
    )


def test_new_dataset_invalid_file(
    caplog,
    cloud_function,
):
    """
    This test ensures that there is an error log when the filetype is invalid.
    """
    caplog.set_level(logging.ERROR)

    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_invalid_file

    cloud_function.new_dataset(cloud_event=cloud_event)

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Invalid filetype received - test_name.pdf"
