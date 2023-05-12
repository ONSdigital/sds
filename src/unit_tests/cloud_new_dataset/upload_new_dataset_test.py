import re
from unittest.mock import MagicMock, call

from pytest import raises
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.dataset.dataset_processor_service import DatasetProcessorService

from src.test_data import dataset_test_data, shared_test_data
from src.unit_tests.test_helper import TestHelper


def test_upload_new_dataset(
    new_dataset_mock,
    get_dataset_from_bucket_mock,
):
    """
    The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
    """
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_data

    DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
    DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            [dataset_test_data.dataset_metadata]
        )
    )

    DatasetFirebaseRepository.create_new_dataset = MagicMock()

    DatasetFirebaseRepository.get_dataset_unit_collection = MagicMock()
    DatasetFirebaseRepository.get_dataset_unit_collection.return_value = (
        dataset_test_data.existing_dataset_unit_data_collection
    )

    DatasetFirebaseRepository.append_unit_to_dataset_units_collection = MagicMock()

    new_dataset_mock(cloud_event=cloud_event)

    DatasetFirebaseRepository.get_latest_dataset_with_survey_id.assert_called_once_with(
        dataset_test_data.survey_id
    )
    DatasetFirebaseRepository.create_new_dataset.assert_called_once_with(
        shared_test_data.test_guid,
        dataset_test_data.updated_dataset_metadata_without_id,
    )

    DatasetFirebaseRepository.get_dataset_unit_collection.assert_called_once_with(
        shared_test_data.test_guid
    )

    append_calls = [
        call(
            dataset_test_data.existing_dataset_unit_data_collection,
            dataset_test_data.dataset_unit_data_collection[0],
        ),
        call(
            dataset_test_data.existing_dataset_unit_data_collection,
            dataset_test_data.dataset_unit_data_collection[1],
        ),
    ]
    DatasetFirebaseRepository.append_unit_to_dataset_units_collection.assert_has_calls(
        append_calls
    )


def test_delete_previous_versions_datasets_success(
    new_dataset_mock, get_dataset_from_bucket_mock
):
    """
    Tests all previous versions of a dataset are deleted when a new dataset version is uploaded to firestore
    """

    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_data

    DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
    DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            [dataset_test_data.dataset_metadata]
        )
    )

    DatasetFirebaseRepository.create_new_dataset = MagicMock()

    DatasetFirebaseRepository.get_dataset_unit_collection = MagicMock()
    DatasetFirebaseRepository.get_dataset_unit_collection.return_value = (
        dataset_test_data.existing_dataset_unit_data_collection
    )

    DatasetFirebaseRepository.append_unit_to_dataset_units_collection = MagicMock()

    DatasetFirebaseRepository.delete_previous_versions_datasets = MagicMock()

    new_dataset_mock(cloud_event=cloud_event)

    DatasetFirebaseRepository.delete_previous_versions_datasets.assert_called_once_with(
        dataset_test_data.survey_id, dataset_test_data.new_dataset_version
    )


def test_delete_previous_versions_datasets_failure(
    new_dataset_mock, get_dataset_from_bucket_mock
):
    """
    Tests an exception is raised if there is an issue deleting previous dataset versions from firestore.
    """

    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_data

    DatasetFirebaseRepository.get_latest_dataset_with_survey_id = MagicMock()
    DatasetFirebaseRepository.get_latest_dataset_with_survey_id.return_value = (
        TestHelper.create_document_snapshot_generator_mock(
            [dataset_test_data.dataset_metadata]
        )
    )

    DatasetFirebaseRepository.create_new_dataset = MagicMock()

    DatasetFirebaseRepository.get_dataset_unit_collection = MagicMock()
    DatasetFirebaseRepository.get_dataset_unit_collection.return_value = (
        dataset_test_data.existing_dataset_unit_data_collection
    )

    DatasetFirebaseRepository.append_unit_to_dataset_units_collection = MagicMock()

    DatasetFirebaseRepository.delete_previous_versions_datasets = MagicMock()
    DatasetFirebaseRepository.delete_previous_versions_datasets.side_effect = Exception

    with raises(
        RuntimeError,
        match="Failed to delete previous dataset versions from firestore.",
    ):
        new_dataset_mock(cloud_event=cloud_event)


def test_empty_datasets_bucket_after_retrieval(
    new_dataset_mock, get_dataset_from_bucket_mock
):
    """
    Tests datasets are deleted from the bucket after they have been retrieved.
    """
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_data

    DatasetBucketRepository.empty_bucket = MagicMock()
    DatasetProcessorService.process_raw_dataset = MagicMock()

    new_dataset_mock(cloud_event=cloud_event)

    DatasetBucketRepository.empty_bucket.assert_called_once()


def test_upload_invalid_file_type(new_dataset_mock, get_dataset_from_bucket_mock):
    """
    Tests the validation for when the file extension is not a json
    """

    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_invalid_filename_data

    DatasetProcessorService.process_raw_dataset = MagicMock()

    with raises(
        RuntimeError,
        match=f"Invalid filetype received - {dataset_test_data.cloud_event_invalid_filename_data['name']}",
    ):
        new_dataset_mock(cloud_event=cloud_event)

    DatasetProcessorService.process_raw_dataset.assert_not_called()


def test_no_dataset_in_bucket(new_dataset_mock):
    """
    Validates when an empty object is returned from the bucket.
    """
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_data

    DatasetProcessorService.process_raw_dataset = MagicMock()

    DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
    DatasetBucketRepository.get_dataset_file_as_json.return_value = None

    with raises(
        RuntimeError,
        match="No corresponding dataset found in bucket",
    ):
        new_dataset_mock(cloud_event=cloud_event)

    DatasetProcessorService.process_raw_dataset.assert_not_called()


def test_missing_dataset_keys(new_dataset_mock):
    """
    Validates when there are missing mandatory keys from the dataset.
    """

    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_data

    DatasetProcessorService.process_raw_dataset = MagicMock()

    DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
    DatasetBucketRepository.get_dataset_file_as_json.return_value = {
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

    DatasetProcessorService.process_raw_dataset.assert_not_called()
