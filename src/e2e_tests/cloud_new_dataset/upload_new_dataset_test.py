from unittest.mock import MagicMock

from repositories.dataset_repository import DatasetRepository

cloud_event_test_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_name.json",
}


def test_upload_new_dataset(new_dataset, dataset_repository_mock):
    """
    There should be a log for when the cloud function is triggered and when the
    new dataset is successfully uploaded.
    """
    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data
    DatasetRepository.get_dataset_with_survey_id = MagicMock()

    new_dataset(cloud_event=cloud_event)

    DatasetRepository.get_dataset_with_survey_id.assert_called_once_with('xyz')
