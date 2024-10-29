from logging_config import logging
from models.dataset_models import (
    DatasetMetadata,
    UnitDataset,
)
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.dataset.dataset_writer_service import DatasetWriterService
from services.validators.query_parameter_validator_service import (
    QueryParameterValidatorService,
)

logger = logging.getLogger(__name__)


class DatasetService:
    def __init__(self) -> None:
        self.dataset_repository = DatasetFirebaseRepository()
        self.dataset_writer_service = DatasetWriterService(self.dataset_repository)


    def get_dataset_metadata_collection(
        self, survey_id: str, period_id: str
    ) -> list[DatasetMetadata]:
        """
        Gets the collection of dataset metadata associated with a specific survey and period id.

        Parameters:
        survey_id (str): survey id of the collection.
        period_id (str): period id of the collection.
        """

        QueryParameterValidatorService.validate_survey_and_period_id_from_dataset_metadata(
            survey_id, period_id
        )

        return self.dataset_repository.get_dataset_metadata_collection(
            survey_id, period_id
        )

    def get_unit_supplementary_data(self, dataset_id, identifier) -> UnitDataset:
        """
        Gets the unit_data of dataset associated with a specific dataset_id and identifier.

        Parameters:
        dataset_id (str): dataset_id of the dataset.
        identifier (str): identifier of the unit.
        """

        unit_supplementary_data = self.dataset_repository.get_unit_supplementary_data(
                dataset_id, identifier)

        return unit_supplementary_data
