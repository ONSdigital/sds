from models.dataset_models import DatasetMetadata, UnitDataset
from repositories.dataset_repository import DatasetRepository


class DatasetReaderService:
    def __init__(self, dataset_repository: DatasetRepository) -> None:
        self.dataset_repository = dataset_repository
        pass

    def get_dataset_with_survey_id(self, survey_id: str) -> list[DatasetMetadata]:
        """
        Returns a dataset associated with a specific survey id.

        Parameters:
        survey_id (str): survey_id used for query match
        """
        return self.dataset_repository.get_dataset_with_survey_id(survey_id)

    def get_dataset_unit_collection(self, dataset_id: str) -> list[UnitDataset]:
        """
        Gets the unit data collection associated with a specific dataset_id

        Parameters:
        dataset_id (str): dataset_id for the new dataset.
        """
        return self.dataset_repository.get_dataset_unit_collection(dataset_id)
