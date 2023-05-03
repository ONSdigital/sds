import logging
from unittest.mock import MagicMock, call

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

    DatasetFirebaseRepository.get_dataset_with_survey_id.assert_called_once_with(
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
    caplog,
):
    caplog.set_level(logging.ERROR)

    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_invalid_filename_test_data

    DatasetProcessorService.process_new_dataset = MagicMock()

    new_dataset_mock(cloud_event=cloud_event)

    assert len(caplog.records) == 1
    assert (
        caplog.records[0].message
        == f"Invalid filetype received - {dataset_test_data.cloud_event_invalid_filename_test_data['name']}"
    )
    DatasetProcessorService.process_new_dataset.assert_not_called()
