from unittest.mock import MagicMock
import uuid
from datetime import datetime

from repositories.dataset_repository import DatasetRepository
from services.datetime_service import DatetimeService

cloud_event_test_data = {
    "id": "test_id",
    "type": "test_type",
    "bucket": "test_bucket",
    "metageneration": "1",
    "timeCreated": "test_time_created",
    "updated": "test_time_updated",
    "name": "test_filename.json",
}


def test_upload_new_dataset(new_dataset):
    """
    There should be a log for when the cloud function is triggered and when the
    new dataset is successfully uploaded.
    """
    cloud_event = MagicMock()
    cloud_event.data = cloud_event_test_data

    DatasetRepository.get_dataset_with_survey_id = MagicMock()
    DatasetRepository.get_dataset_with_survey_id.return_value = [{
        "dataset_id": "test_dataset_id",
        "survey_id": "xyz",
        "period_id": "abc",
        "title": "Which side was better?",
        "sds_schema_version": 4,
        "sds_published_at": "2023-04-20T12:00:00Z",
        "total_reporting_units": 1,
        "schema_version": "v1.0.0",
        "sds_dataset_version": 1,
        "filename": "test_filename.json",
        "form_type": "yyy",
    }]

    DatasetRepository.create_new_dataset = MagicMock()
    DatasetRepository.create_new_dataset.return_value = None

    uuid.uuid4 = MagicMock()
    uuid.uuid4.return_value = "test_dataset_id"

    test_date = datetime(2023, 4, 20, 12, 0, 0)
    DatetimeService.get_current_date_and_time = MagicMock()
    DatetimeService.get_current_date_and_time.return_value = test_date

    new_dataset(cloud_event=cloud_event)

    DatasetRepository.get_dataset_with_survey_id.assert_called_once_with("xyz")
    DatasetRepository.create_new_dataset.assert_called_once_with(
        "test_dataset_id",
        {
            "survey_id": "xyz",
            "period_id": "abc",
            "title": "Which side was better?",
            "sds_schema_version": 4,
            "sds_published_at": "2023-04-20T12:00:00Z",
            "total_reporting_units": 2,
            "schema_version": "v1.0.0",
            "sds_dataset_version": 2,
            "filename": "test_filename.json",
            "form_type": "yyy",
        }
    )
