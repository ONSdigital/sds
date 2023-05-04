import re
from unittest.mock import MagicMock, call

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.dataset.dataset_processor_service import DatasetProcessorService

from src.test_data import dataset_test_data, shared_test_data


def test_upload_new_dataset(
    new_dataset_mock, uuid_mock, datetime_mock, dataset_repository_boundaries_mock
):
    """
    The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
    """
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_test_data

    new_dataset_mock(cloud_event=cloud_event)

    DatasetFirebaseRepository.get_latest_dataset_with_survey_id.assert_called_once_with(
        dataset_test_data.test_survey_id
    )
    DatasetFirebaseRepository.create_new_dataset.assert_called_once_with(
        shared_test_data.test_guid,
        dataset_test_data.dataset_metadata_without_id,
    )

    DatasetFirebaseRepository.get_dataset_unit_collection.assert_called_once_with(
        shared_test_data.test_guid
    )

    append_calls = [
        call(
            dataset_test_data.existing_dataset_unit_data_collection,
            dataset_test_data.new_dataset_unit_data_collection[0],
        ),
        call(
            dataset_test_data.existing_dataset_unit_data_collection,
            dataset_test_data.new_dataset_unit_data_collection[1],
        ),
    ]
    DatasetFirebaseRepository.append_unit_to_dataset_units_collection.assert_has_calls(
        append_calls
    )


def test_upload_invalid_filename(
    new_dataset_mock,
):
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_invalid_filename_test_data

    DatasetProcessorService.process_new_dataset = MagicMock()

    with raises(
        RuntimeError,
        match=f"Invalid filetype received - {dataset_test_data.cloud_event_invalid_filename_test_data['name']}",
    ):
        new_dataset_mock(cloud_event=cloud_event)

    DatasetProcessorService.process_new_dataset.assert_not_called()


def test_no_dataset_in_bucket(
    new_dataset_mock,
):
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_test_data

    DatasetProcessorService.process_new_dataset = MagicMock()

    DatasetBucketRepository.get_bucket_file_as_json = MagicMock()
    DatasetBucketRepository.get_bucket_file_as_json.return_value = None

    with raises(
        RuntimeError,
        match="No corresponding dataset found in bucket",
    ):
        new_dataset_mock(cloud_event=cloud_event)

    DatasetProcessorService.process_new_dataset.assert_not_called()


def test_missing_dataset_keys(new_dataset_mock):
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_test_data

    DatasetProcessorService.process_new_dataset = MagicMock()

    DatasetBucketRepository.get_bucket_file_as_json = MagicMock()
    DatasetBucketRepository.get_bucket_file_as_json.return_value = {
        "period_id": "test_period_id",
        "sds_schema_version": "test_sds_schema_version",
        "schema_version": 1,
        "form_type": "test_form_type",
        "data": "test_data",
    }

    with raises(
        RuntimeError,
        match=re.escape("Mandatory key(s) missing from JSON: survey_id."),
    ):
        new_dataset_mock(cloud_event=cloud_event)

    DatasetProcessorService.process_new_dataset.assert_not_called()
