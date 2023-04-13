import json
from unittest.mock import MagicMock

from config import config
from google.cloud import storage as google_cloud_storage


def test_new_dataset(cloud_functions, database, monkeypatch):
    """
    Checks that fastAPI accepts a valid schema file
    and returns a valid schema metadata file.
    """
    monkeypatch.setattr(google_cloud_storage, "Client", MagicMock())

    cloud_event = MagicMock()
    cloud_event.data = {
        "id": "7092733353352312",
        "type": "google.cloud.storage.object.v1.finalized",
        "bucket": "dataset_bucket",
        "metageneration": "1",
        "timeCreated": "2023-03-01T14:40:37.896Z",
        "updated": "2023-03-01T14:40:37.896Z",
        "name": "123e4567-e89b-12d3-a456-426614174000.json",
    }
    with open(config.TEST_DATASET_PATH) as f:
        dataset_with_meta = json.load(f)
    mock_storage_client = MagicMock()
    cloud_functions.dataset_storage.storage_client = mock_storage_client
    mock_storage_client.bucket().blob().download_as_string.return_value = json.dumps(
        dataset_with_meta, indent=2
    )
    database.datasets_collection.where().order_by().limit().stream().__next__().to_dict.return_value = {
        "sds_dataset_version": 25
    }
    cloud_functions.new_dataset(cloud_event=cloud_event)
