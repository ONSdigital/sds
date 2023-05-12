import json
from typing import Generator
from unittest.mock import MagicMock

from config.config_factory import ConfigFactory
from google.cloud.firestore_v1.document import DocumentSnapshot
from models.dataset_models import UnitDataset
from repositories.buckets.dataset_bucket_repository import DatasetBucketRepository

config = ConfigFactory.get_config()


class TestHelper:
    @staticmethod
    def new_dataset_mock(cloud_event):
        """
        Mocks the cloud function call.
        """
        from main import new_dataset

        return new_dataset(cloud_event)

    @staticmethod
    def mock_get_dataset_from_bucket():
        """
        Mocks the application's google bucket boundaries.
        """
        with open(config.TEST_DATASET_PATH) as f:
            dataset_with_metadata: UnitDataset = json.load(f)

        DatasetBucketRepository.get_dataset_file_as_json = MagicMock()
        DatasetBucketRepository.get_dataset_file_as_json.return_value = (
            dataset_with_metadata
        )

    @staticmethod
    def create_document_snapshot_generator_mock(
        yield_data_collection,
    ) -> Generator[DocumentSnapshot, None, None]:
        """
        When firestore data is streamed via their SDK, it returns a generator of a DocumentSnapshot. This helper function
        simulates the functionality of the generator to be used in tests.
        """

        id_count = 0
        for data in yield_data_collection:
            generator_wrapper = MagicMock(spec=DocumentSnapshot)
            generator_wrapper.id = f"id_{id_count}"
            id_count += 1
            generator_wrapper.to_dict.return_value = data

            yield generator_wrapper
