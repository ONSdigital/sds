from unittest.mock import MagicMock, call

from repositories.dataset_repository import DatasetRepository

from src.test_data.new_dataset import dataset_test_data


def test_upload_new_dataset(
    new_dataset_mock, uuid_mock, datetime_mock, dataset_repository_boundaries_mock
):
    """
    The e2e journey for when a new dataset is uploaded, with repository boundaries, uuid generation and datetime mocked.
    """
    cloud_event = MagicMock()
    cloud_event.data = dataset_test_data.cloud_event_test_data

    new_dataset_mock(cloud_event=cloud_event)

    DatasetRepository.get_dataset_with_survey_id.assert_called_once_with(
        dataset_test_data.test_survey_id
    )
    DatasetRepository.create_new_dataset.assert_called_once_with(
        dataset_test_data.test_dataset_id,
        dataset_test_data.dataset_metadata_without_id,
    )

    DatasetRepository.get_dataset_unit_collection.assert_called_once_with(
        dataset_test_data.test_dataset_id
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
    DatasetRepository.append_unit_to_dataset_units_collection.assert_has_calls(
        append_calls
    )
