import uuid

from config.config_factory import config
from logging_config import logging
from models.dataset_models import (
    DatasetMetadata,
    UnitDataset,
)
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.shared.datetime_service import DatetimeService
from services.shared.document_version_service import DocumentVersionService

logger = logging.getLogger(__name__)


class DatasetProcessorService:
    def __init__(self) -> None:
        self.dataset_repository = DatasetFirebaseRepository()

    def get_dataset_metadata_collection(
        self, survey_id: str, period_id: str
    ) -> list[DatasetMetadata]:
        """
        Gets the collection of dataset metadata associated with a specific survey and period id.

        Parameters:
        survey_id (str): survey id of the collection.
        period_id (str): period id of the collection.
        """
        return self.dataset_repository.get_dataset_metadata_collection(
            survey_id, period_id
        )

    def get_unit_supplementary_data(
        self, dataset_id: str, identifier: str
    ) -> UnitDataset:
        """
        Retrieve supplementary data for a particular unit given the dataset id and identifier.

        Parameters:
        dataset_id (str): The dataset id.
        identifier (str): The identifier of the unit.
        """
        return self.dataset_repository.get_unit_supplementary_data(
            dataset_id, identifier
        )
